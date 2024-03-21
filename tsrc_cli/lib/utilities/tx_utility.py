from algosdk import account, mnemonic
from algosdk.transaction import PaymentTxn, SuggestedParams

class AlgorandAccount:
    def __init__(self, mnemonic_phrase=None):
        if mnemonic_phrase is None:
            self.private_key, self.address = account.generate_account()
            self.mnemonic = mnemonic.from_private_key(self.private_key)
        else:
            self.private_key = mnemonic.to_private_key(mnemonic_phrase)
            self.address = account.address_from_private_key(self.private_key)
            self.mnemonic = mnemonic_phrase

    def create_account_txn(self, sponsor, params, initial_funds):
        try:
            # Create the payment transaction
            txn = PaymentTxn(
                sender=sponsor.address,
                sp=params,
                receiver=self.address,
                amt=initial_funds
            )
            return txn
        except Exception as e:
            print(f"Error creating account transaction: {e}")
            return None

    def verify_address_ownership(self, address):
        try:
            # Derive the account from the mnemonic
            derived_private_key = mnemonic.to_private_key(self.mnemonic)
            derived_address = account.address_from_private_key(derived_private_key)

            # Compare the derived address with the given address
            if derived_address == address:
                print("Address ownership verified!")
                return True
            else:
                print("Address does not belong to the provided mnemonic.")
                return False
        except Exception as e:
            print(f"Error occurred while verifying address ownership: {str(e)}")
            return False

class TransactionSigner:
    @staticmethod
    def sign_transaction(txn, signer):
        try:
            signed_txn = txn.sign(signer.private_key)
            return signed_txn
        except Exception as e:
            print(f"Error signing transaction: {e}")
            return None
