import base64
from algosdk import transaction, account, mnemonic
from algosdk.encoding import encode_address, decode_address
from algosdk.v2client import algod
from algosdk.transaction import AssetTransferTxn, ApplicationCallTxn, StateSchema
from algosdk.transaction import SuggestedParams


def create_repo(account, asset_id, approval_program, clear_program):
    sender = account.address

    # Create a dummy SuggestedParams object with default values
    dummy_params = SuggestedParams(
        fee=0,
        flat_fee=True,
        first=0,
        last=0,
        gh="",
        gen="",
        consensus_version="",
        min_fee=0
    )

    global_ints = 24
    global_bytes = 11
    local_ints = 0
    local_bytes = 0

    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    app_args = [intToBytes(1000000)]  # TotalSupply as an app argument

    txn = transaction.ApplicationCreateTxn(
        sender,
        dummy_params,  # Use the dummy SuggestedParams object
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

from tsrc_cli.lib.utilities.utility import (
    wait_for_confirmation,
    wait_for_round,
    get_private_key_from_mnemonic,
    intToBytes,
    opt_in_asa,
    opt_in_app,
    call_app,
    read_global_state
)

def create_repo(account, asset_id, approval_program, clear_program):
    sender = account.address

    # Create a dummy SuggestedParams object with default values
    dummy_params = SuggestedParams(
        fee=0,
        flat_fee=True,
        first=0,
        last=0,
        gh="",
        gen="",
        consensus_version="",
        min_fee=0
    )

    global_ints = 24
    global_bytes = 11
    local_ints = 0
    local_bytes = 0

    global_schema = StateSchema(global_ints, global_bytes)
    local_schema = StateSchema(local_ints, local_bytes)

    app_args = [intToBytes(1000000)]  # TotalSupply as an app argument

    txn = transaction.ApplicationCreateTxn(
        sender,
        dummy_params,  # Use the dummy SuggestedParams object
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
