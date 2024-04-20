import base64
import re
from algosdk import encoding, transaction, account, mnemonic
from algosdk.transaction import AssetTransferTxn, ApplicationCreateTxn, ApplicationOptInTxn, ApplicationCallTxn, ApplicationDeleteTxn, ApplicationCloseOutTxn, ApplicationClearStateTxn
from algosdk.v2client import algod

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response["result"])


# helper function that converts a mnemonic passphrase into a private signing key
def get_private_key_from_mnemonic(mn):
    private_key = mnemonic.to_private_key(mn)
    return private_key


# helper function that waits for a given txid to be confirmed by the network
def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


def wait_for_round(client, round):
    last_round = client.status().get("last-round")
    print(f"Waiting for round {round}")
    while last_round < round:
        last_round += 1
        client.status_after_block(last_round)
        print(f"Round {last_round}")

# opt-in to application
def opt_in_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("OptIn from account: ", sender)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationOptInTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("OptIn to app-id:", transaction_response["txn"]["txn"]["apid"])

# Function to opt-in to an ASA (commented out by default)
def opt_in_asa(client, private_key, asset_id):
    """
    Opt-in to an ASA for the account associated with the provided private key.

    Args:
        client (AlgodClient): An instance of the Algod client.
        private_key (str): The private key of the account opting in.
        asset_id (int): The ID of the ASA to opt-in.
    """
    # Define sender
    sender = account.address_from_private_key(private_key)

    # Get node suggested parameters
    params = client.suggested_params()

    # Create the asset opt-in transaction
    optin_txn = AssetTransferTxn(
        sender=sender,
        sp=params,
        receiver=sender,
        amt=0,
        index=asset_id
    )

    # Sign the transaction
    signed_optin_txn = optin_txn.sign(private_key)

    # Send the transaction
    txid = client.send_transaction(signed_optin_txn)

    # Await confirmation
    wait_for_confirmation(client, txid)
    print(f"Opted-in to asset {asset_id}.")

def format_state(state):
    formatted = {}
    for item in state:
        key = item["key"]
        value = item["value"]
        try:
            # Try decoding as UTF-8. If it fails, handle as binary data
            formatted_key = base64.b64decode(key).decode("utf-8")
        except UnicodeDecodeError:
            # If it's not a UTF-8 string, it might be binary data like an address
            formatted_key = base64.b64decode(key).hex()  # Represent binary data in hex

        if value["type"] == 1:
            # byte string
            try:
                # Try decoding value as UTF-8
                formatted_value = base64.b64decode(value["bytes"]).decode("utf-8")
            except UnicodeDecodeError:
                # If it's not a UTF-8 string, handle as binary data
                formatted_value = base64.b64decode(value["bytes"]).hex()  # Represent binary data in hex
        else:
            # integer
            formatted_value = value["uint"]

        formatted[formatted_key] = formatted_value

    return format_state_other_cases(formatted)

def hex_to_algorand_address(hex_data):
    try:
        address_bytes = bytes.fromhex(hex_data)
        address = encoding.encode_address(address_bytes)
        return address
    except Exception as e:
        return f"Error: {str(e)}"

# Converts and formats the keys and values of an Algorand application's global state, decoding
# hexadecimal strings to human-readable Algorand addresses and managing various data types.
def format_state_other_cases(state):
    formatted = {}
    for key, value in state.items():
        if key.startswith("566f74655f"):  # Prefix like "Vote_"
            print(f"Processing 'Vote_' prefixed key: {key}")
            remaining_key = key[len("566f74655f"):]
            address = remaining_key[-64:]
            choice_hex = remaining_key[:-64]
            try:
                choice = bytes.fromhex(choice_hex).decode("utf-8")
                choice = choice.rstrip("_")  # Remove any trailing underscore
            except Exception as e:
                print(f"Error decoding choice: {e}")
                choice = choice_hex
            print(f"Split into choice: {choice}, address: {address}")
            if re.match("^[0-9a-fA-F]{64}$", address):
                formatted_address = hex_to_algorand_address(address)
                formatted_key = f"Vote_{choice}_{formatted_address}"
                formatted[formatted_key] = value
                print(f"Formatted key: {formatted_key}")
            else:
                print(f"Address part does not match expected format")
        elif isinstance(value, int):
            formatted[key] = value
            print(f"Integer value for key {key}, keeping as is: {value}")
        else:
            try:
                # Check if key is a 64-character hexadecimal string and not prefixed
                if re.match("^[0-9a-fA-F]{64}$", key):
                    address = hex_to_algorand_address(key)
                    formatted[address] = value
                elif re.match("^[0-9a-fA-F]{64}$", value):
                    # Handle cases where the value is a 64-character hex string
                    formatted[key] = hex_to_algorand_address(value)
                else:
                    # Keep original key-value pair if conversion is not applicable
                    formatted[key] = value
            except Exception as e:
                # Keep original key-value pair if conversion fails
                print(f"Exception occurred for key {key}: {e}")
                formatted[key] = value
    return formatted

# read user local state
def read_local_state(client, addr, app_id):
    results = client.account_info(addr)
    for local_state in results["apps-local-state"]:
        if local_state["id"] == app_id:
            if "key-value" not in local_state:
                return {}
            return format_state(local_state["key-value"])
    return {}


# read app global state
def read_global_state(client, app_id):
    # Fetch application information
    app_info = client.application_info(app_id)

    # Check if the application information is available
    if "params" in app_info and "global-state" in app_info["params"]:
        return format_state(app_info["params"]["global-state"])

    return {}

# Modify the call_app function to include foreign_assets
def call_app(client, private_key, app_id, app_args):
    # declare sender
    sender = account.address_from_private_key(private_key)
    print("Call from account:", sender)

    # get node suggested parameters
    params = client.suggested_params()

    # Include Asset 1653 in the foreign assets for the transaction
    foreign_assets = [1653]  # Asset ID to be included

    # create unsigned transaction
    txn = transaction.ApplicationCallTxn(
        sender,
        params,
        app_id,
        transaction.OnComplete.NoOpOC,  # Specify the type of application call
        app_args=app_args,
        foreign_assets=foreign_assets  # Add this line
    )

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

# delete application
def delete_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationDeleteTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Deleted app-id:", transaction_response["txn"]["txn"]["apid"])


# close out from application
def close_out_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationCloseOutTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Closed out from app-id: ", transaction_response["txn"]["txn"]["apid"])


# clear application
def clear_app(client, private_key, index):
    # declare sender
    sender = account.address_from_private_key(private_key)

    # get node suggested parameters
    params = client.suggested_params()
    # comment out the next two (2) lines to use suggested fees
    params.flat_fee = True
    params.fee = 1000

    # create unsigned transaction
    txn = transaction.ApplicationClearStateTxn(sender, params, index)

    # sign transaction
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()

    # send transaction
    client.send_transactions([signed_txn])

    # await confirmation
    wait_for_confirmation(client, tx_id)

    # display results
    transaction_response = client.pending_transaction_info(tx_id)
    print("Cleared app-id:", transaction_response["txn"]["txn"]["apid"])


# convert 64 bit integer i to byte string
def intToBytes(i):
    return i.to_bytes(8, 'big')  # Convert integer to 8-byte big-endian
