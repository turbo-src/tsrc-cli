import base64
from algosdk import transaction, account, mnemonic
from algosdk.encoding import encode_address, decode_address
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, ApplicationCallTxn, StateSchema

from lib.utilities.utility import (
    wait_for_confirmation,
    wait_for_round,
    get_private_key_from_mnemonic,
    intToBytes,
    opt_in_asa,
    opt_in_app,
    call_app,
    read_global_state
)

class Vote:
    def __init__(self, algod_address, algod_token, asset_id, creator_mnemonic, user_mnemonic, app_id=None):
        self.client = algod.AlgodClient(algod_token, algod_address)
        self.creator_private_key = get_private_key_from_mnemonic(creator_mnemonic)
        self.user_private_key = get_private_key_from_mnemonic(user_mnemonic)
        self.asset_id = asset_id
        self.global_ints = 24  # Adjust as needed
        self.global_bytes = 11  # Adjust as needed
        self.local_ints = 0
        self.local_bytes = 0
        self.status = self.client.status()
        self.regBegin = self.status["last-round"] + 10
        self.regEnd = self.regBegin + 10
        self.voteBegin = self.regEnd + 1
        self.voteEnd = self.voteBegin + 10
        self.app_id = app_id if app_id is not None else None

        # Shouldn't be needed at all
        opt_in_asa(self.client, self.creator_private_key, self.asset_id)

        with open('vote_approval.teal.tok', 'rb') as f:
            self.approval_program = f.read()

        with open('vote_clear_state.teal.tok', 'rb') as f:
            self.clear_program = f.read()

    def create_repo(account, app_args=None):
        sender = account.address
        params = algod_client.suggested_params()
        params.flat_fee = True
        params.fee = 1000

        global_ints = 24
        global_bytes = 11
        local_ints = 0
        local_bytes = 0

        global_schema = StateSchema(global_ints, global_bytes)
        local_schema = StateSchema(local_ints, local_bytes)

        app_args = [intToBytes(1000000)]  # TotalSupply as an app argument

        txn = transaction.ApplicationCreateTxn(
            sender,
            params,
            transaction.OnComplete.NoOpOC.real,
            approval_program,
            clear_program,
            global_schema,
            local_schema,
            app_args,
        )
    
        signed_txn = txn.sign(account.private_key)
    
        return signed_txn

    def optin(self):
        opt_in_app(self.client, self.user_private_key, self.app_id)

    def read_global_state(self):

        return read_global_state(self.client, self.app_id)

    def vote(self, app_args=None):
        sender = account.address_from_private_key(self.creator_private_key)

        # call application without arguments
        call_app(self.client, self.user_private_key, self.app_id, app_args)

        # read global state of application
        global_state = read_global_state(self.client, self.app_id)

        print(f"Global state: {global_state}")

        # Safely get the 'Winner' key from the global state
        winner = global_state.get("Winner")

        if winner:
            print("The winner is:", winner)
        else:
            print("No winner declared yet")


        return global_state

    def delete_global_state_key_human(self, choice, sender):
        # Get the sender's account address
        sender_address = account.address_from_private_key(self.creator_private_key)
    
        # Get the suggested parameters for the transaction
        params = self.client.suggested_params()
    
        # Decode the sender's Algorand address to bytes
        sender_bytes = decode_address(sender)
    
        # Construct the key using the decoded sender bytes
        key = f"Vote_{choice}_".encode() + sender_bytes
    
        # Create the application call transaction
        app_args = [
            "delete_key".encode("utf-8"),
            key
        ]
        call_txn = ApplicationCallTxn(
            sender=sender_address,
            sp=params,
            index=self.app_id,
            app_args=app_args,
            on_complete=transaction.OnComplete.NoOpOC
        )
    
        # Sign the transaction with the sender's private key
        signed_txn = call_txn.sign(self.creator_private_key)
    
        # Send the transaction to the network
        txid = self.client.send_transaction(signed_txn)
    
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(self.client, txid)
    
        print(f"Deleted key '{key}' from the global state of app with ID: {self.app_id}")
        print(f"Transaction ID: {txid}")
 
    def delete_key(self, key_args):
        if not self.app_id:
            raise Exception("Application ID not set")
    
        # Assuming key_args is a list where the first element is the action and the second is the key name
        action = key_args[0]
        key_name = key_args[1]
    
        # Prepare the arguments for the application call
        app_args = [action, key_name]
    
        # Use call_app function to send the transaction
        call_app(self.client, self.creator_private_key, self.app_id, app_args)
    
        # Optionally, you can read and return the global state to verify the deletion
        global_state = read_global_state(self.client, self.app_id)
        return global_state

    def delete_keys_associated_with_choice(self, choice):
        global_state = read_global_state(self.client, self.app_id)

        if "Winner" not in global_state:
            raise ValueError("No 'Winner' key found in the global state.")

        if global_state["Winner"] != choice:
            raise ValueError(f"The specified choice '{choice}' is not the winner.")

        keys_to_delete = []
        vote_keys_to_delete = []

        for key in global_state.keys():
            if choice in key:
                if key.startswith("Exclusive_"):
                    continue  # Skip keys starting with "Exclusive_"
                elif key.startswith("Vote_"):
                    vote_keys_to_delete.append(key)
                else:
                    keys_to_delete.append(key)

        # Explicitly delete the "Winner" key if the specified choice matches the value of the "Winner" key
        if global_state["Winner"] == choice:
            keys_to_delete.append("Winner")

        for key in keys_to_delete:
            self.delete_key([b"delete_key", key.encode()])

        for key in vote_keys_to_delete:
            sender = key.split("_")[-1]
            self.delete_global_state_key_human(choice, sender)

        print(f"Deleted keys associated with choice '{choice}'.")
