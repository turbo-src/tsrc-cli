import base64
from algosdk import transaction, account, mnemonic
from algosdk.encoding import encode_address, decode_address
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, ApplicationCallTxn, StateSchema, SuggestedParams, ApplicationCreateTxn


def create_repo(client, account, asset_id, approval_program, clear_program):
    sender = account.address

    # Create a dummy SuggestedParams object with manual values
    params = client.suggested_params()
    #dummy_params = transaction.SuggestedParams(
    #    fee=1000,
    #    flat_fee=False,
    #    first=10000,
    #    last=11000,
    #    gh=b'dbf9c2e4007d7c46fc755f02f1ca80a6ffecc7a58fcff3067c0d6df810b9f33f',
    #    gen="private-v1",
    #    consensus_version="https://github.com/algorandfoundation/specs/tree/master/dev",
    #    min_fee=1000
    #)

    global_ints = 24
    global_bytes = 11
    local_ints = 0
    local_bytes = 0

    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)

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
        foreign_assets=[asset_id]
    )

    signed_txn = txn.sign(account.private_key)

    return signed_txn

def vote_repo(client, mnemonic, app_id, choice, asset_id, commit_id):
    asset_id = int(asset_id)
    print("asset_id", asset_id)
    private_key = get_private_key_from_mnemonic(mnemonic)
    print("Using private key:", private_key)
    sender = account.address_from_private_key(private_key)
    print("Call from account:", sender)

    opt_in_app(client, private_key, app_id)

    params = client.suggested_params()

    # Prepare the application arguments
    app_args = [
        b"vote",
        choice.encode(),
        commit_id.encode()
    ]

    # Create the ApplicationCallTxn
    txn = transaction.ApplicationCallTxn(
        sender,
        params,
        app_id,
        transaction.OnComplete.NoOpOC.real,
        app_args=app_args,
        foreign_assets=[asset_id]
    )

    signed_txn = txn.sign(private_key)

    return signed_txn

from tsrc_cli.lib.utilities.utility import (
    wait_for_confirmation,
    wait_for_round,
    get_private_key_from_mnemonic,
    intToBytes,
    opt_in_asa,
    opt_in_app,
    #call_app,
    read_global_state
)

from tsrc_cli.lib.utilities.tx_utility import (
    AlgorandAccount
)

