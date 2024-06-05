import sys
import requests
import click
from algosdk.v2client import algod
from algosdk import transaction, encoding
from tsrc_cli.lib.create_user import create_user, parse_create_user_response
from tsrc_cli.lib.get_user import get_user, parse_get_user_response
from tsrc_cli.lib.get_user_by_name import get_user_by_name, parse_get_user_by_name_response
from tsrc_cli.lib.create_repo import parse_create_repo_response
from tsrc_cli.lib.get_repo import get_repo, parse_get_repo_response  # Import the new functions
from tsrc_cli.lib.vote_repo import vote_repo, parse_vote_repo_response
from tsrc_cli.lib.get_tsrcid import get_tsrcid
from tsrc_cli.lib.get_tsrckey import get_tsrckey
from tsrc_cli.lib.utilities.tx_utility import AlgorandAccount
from tsrc_cli.lib.blockchain.blockchain import create_repo
from tsrc_cli.lib.blockchain.blockchain import vote_repo
from tsrc_cli.lib.utilities.utility import wait_for_confirmation
import base64
import msgpack

@click.group()
def cli():
    pass

@cli.group(name="user")
def user():
    pass

@cli.group(name="repo")
def repo():
    pass

@user.command(name="create")
@click.argument('contributor-name')
@click.option('--contributor-mnemonic', '-m', help='Contributor mnemonic', required=False)
def create_user_cmd(contributor_name, contributor_mnemonic):
    if not contributor_mnemonic:
        sys.stderr.write("Error: Contributor mnemonic is required.\n")
        sys.exit(1)

    # Create an instance of AlgorandAccount for the new account (user) with the provided mnemonic
    account = AlgorandAccount(mnemonic_phrase=contributor_mnemonic)
    contributor_id = account.address

    response = create_user(contributor_id, contributor_name, "deprecating_password_for_unsigned_tx")
    status, parsed_response = parse_create_user_response(response)

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

@user.command(name="get")
@click.argument('contributor-name', required=False)
@click.option('--contributor-id', '-i', help='Contributor ID', required=False)
def get_user_cmd(contributor_name, contributor_id):
    if contributor_id:
        response = get_user(contributor_id)
        status, parsed_response = parse_get_user_response(response)
    else:
        if not contributor_name:
            sys.stderr.write("Error: Contributor name or ID is required.\n")
            sys.exit(1)
        
        response = get_user_by_name(contributor_name)
        status, parsed_response = parse_get_user_by_name_response(response)
    
    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

@repo.command(name="create")
@click.argument('contributor-name')
@click.option('--contributor-mnemonic', '-m', help='Contributor mnemonic', required=False)
def create_repo_cmd(contributor_name, contributor_mnemonic):
    #print("Inside create_repo_cmd function")
    if not contributor_mnemonic:
        sys.stderr.write("Error: Contributor mnemonic is required.\n")
        sys.exit(1)

    # Create an instance of AlgorandAccount for the new account (user) with the provided mnemonic
    #print("Creating AlgorandAccount instance")
    account = AlgorandAccount(mnemonic_phrase=contributor_mnemonic)
    contributor_id = account.address
    #print(f"Contributor ID: {contributor_id}")

    with open('vote_approval.teal.tok', 'rb') as f:
        approval_program = f.read()

    with open('vote_clear_state.teal.tok', 'rb') as f:
        clear_program = f.read()
    #print("Loaded approval and clear programs")

    import json
    # Load the configuration file
    with open('config/config.json', 'r') as file:
        config = json.load(file)

    # Accessing specific configuration data
    creator_mnemonic = config['creatorInfo']['mnemonic']
    algod_token = config['algodToken']
    algod_address = config['algodAddress']
    asset_id = config['assetId']
    client = algod.AlgodClient(algod_token, algod_address)

    # Sign the transaction using the create_repo function from blockchain.py
    #print("Signing the transaction")
    signed_txn = create_repo(client, account, asset_id, approval_program=approval_program, clear_program=clear_program)
    #print("Transaction signed")

    # Assuming `signed_txn` is your SignedTransaction object
    #print("Type of signed_txn:", type(signed_txn))

    # Convert the signed transaction to a dictionary
    txn_dict = signed_txn.dictify()
    
    # Serialize the transaction dictionary using msgpack
    serialized_txn = msgpack.packb(txn_dict)
    
    # Confirm the type to ensure it's bytes
    #print(f"Serialized transaction type: {type(serialized_txn)}")
    
    # Encode the serialized transaction to base64
    base64_txn = base64.b64encode(serialized_txn).decode('utf-8')
    
    # Print the base64 encoded transaction
    #print(f"Base64 encoded transaction: {base64_txn}")

    ## Print the signed_txn object
    #print("Signed transaction object:", signed_txn)
    #print("Transaction ID:", signed_txn.transaction.get_txid())

    # Encode the signed_txn
    encoded_txn = encoding.msgpack_encode(signed_txn)
    #print("Encoded signed transaction:", encoded_txn)

    # Decode the encoded_txn
    decoded_txn = encoding.msgpack_decode(encoded_txn)
    #print("Decoded transaction object:", decoded_txn)
    #print("Decoded transaction type:", type(decoded_txn))
    #print("Decoded transaction:")
    #print("  Transaction ID:", decoded_txn.transaction.get_txid())
    #print("  Sender:", decoded_txn.transaction.sender)
    #print("  Application ID:", decoded_txn.transaction.index)
    #print("  Fee:", decoded_txn.transaction.fee)
    #print("  First Valid:", decoded_txn.transaction.first_valid_round)
    #print("  Last Valid:", decoded_txn.transaction.last_valid_round)
    #print("  Genesis Hash:", decoded_txn.transaction.genesis_hash)
    #print("  Genesis ID:", decoded_txn.transaction.genesis_id)
    #print("  Group:", decoded_txn.transaction.group)
    #print("  Lease:", decoded_txn.transaction.lease)
    #print("  Note:", decoded_txn.transaction.note)
    #print("  Rekey To:", decoded_txn.transaction.rekey_to)
    #print("  Type:", decoded_txn.transaction.type)
    
    #if hasattr(decoded_txn.transaction, 'approval_program'):
    #    print("  Approval Program:", decoded_txn.transaction.approval_program)
    #if hasattr(decoded_txn.transaction, 'clear_state_program'):
    #    print("  Clear State Program:", decoded_txn.transaction.clear_state_program)
    #if hasattr(decoded_txn.transaction, 'app_args'):
    #    print("  App Arguments:", decoded_txn.transaction.app_args)
    #if hasattr(decoded_txn.transaction, 'accounts'):
    #    print("  Accounts:", decoded_txn.transaction.accounts)
    #if hasattr(decoded_txn.transaction, 'foreign_apps'):
    #    print("  Foreign Apps:", decoded_txn.transaction.foreign_apps)
    #if hasattr(decoded_txn.transaction, 'foreign_assets'):
    #    print("  Foreign Assets:", decoded_txn.transaction.foreign_assets)
    #if hasattr(decoded_txn.transaction, 'global_state_schema'):
    #    print("  Global State Schema:", decoded_txn.transaction.global_state_schema)
    #if hasattr(decoded_txn.transaction, 'local_state_schema'):
    #    print("  Local State Schema:", decoded_txn.transaction.local_state_schema)
    #if hasattr(decoded_txn.transaction, 'extra_program_pages'):
    #    print("  Extra Program Pages:", decoded_txn.transaction.extra_program_pages)

    ## Veify the decoded transaction
    ##print("Verifying the decoded transaction...")
    ##print("Decoded transaction type:", type(decoded_txn))
    ##print("Decoded transaction:", decoded_txn)
    ##print("Transaction ID:", decoded_txn.transaction.get_txid())
    ##print("Sender:", decoded_txn.transaction.sender)
    ##print("Application ID:", decoded_txn.transaction.index)

    ## Send the signed transaction
    ##print("Sending the signed transaction")
    #tx_id = signed_txn.transaction.get_txid()
    ##print(f"Get ID of signed-tx: {tx_id}")
    #tx_id = client.send_transaction(signed_txn)
    ##print(f"Transaction sent with ID: {tx_id}")
    #wait_for_confirmation(client, tx_id)
    #response = client.pending_transaction_info(tx_id)
    #app_id = response['application-index']
    ##print("Created new app-id:", app_id)

    CONFIG = {'url': 'http://localhost:4000/graphql/'}  # Corrected URL

    # Send the signed transaction to the endpoint
    #print("Sending the signed transaction to the endpoint")
    response = requests.post(
        CONFIG['url'],
        json={
            'query': f'''
            {{
                createRepo(contributor_id: "{contributor_id}", repo_name: "{contributor_name}", contributor_password: "{base64_txn}") {{
                    status
                    message
                    repoName
                    repoID
                    repoSignature
                }}
            }}
            '''
        },
        headers={'accept': 'json'}
    )
    #print("Response received from the endpoint")

    status, parsed_response = parse_create_repo_response(response)
    #print(f"Status: {status}")
    #print(f"Parsed response: {parsed_response}")

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

@repo.command(name="get")
@click.argument('repo-name', required=False)
@click.option('--repo-id', '-i', help='Repo ID', required=False)
def get_repo_cmd(repo_name, repo_id):
    print(f"get_repo_cmd called with repo_name: {repo_name}, repo_id: {repo_id}")  # Print the input arguments
    if repo_id:
        response = get_repo(repo_id=repo_id)
        print(f"Response from get_repo with repo_id: {response.text}")  # Print the response text
        status, parsed_response = parse_get_repo_response(response)
    else:
        if not repo_name:
            sys.stderr.write("Error: Repo name or ID is required.\n")
            sys.exit(1)

        response = get_repo(repo_name=repo_name)
        print(f"Response from get_repo with repo_name: {response.text}")  # Print the response text
        status, parsed_response = parse_get_repo_response(response)

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

@repo.command(name="vote")
@click.argument('url', required=True)
@click.argument('commit-id', required=True)
@click.argument('app-id', required=True)
def vote_repo_cmd(url, commit_id, app_id):
    import json
    # Load the configuration file
    with open('config/config.json', 'r') as file:
        config = json.load(file)

    # Accessing specific configuration data
    mnemonic = config['creatorInfo']['mnemonic']
    algod_token = config['algodToken']
    algod_address = config['algodAddress']
    asset_id = config['assetId']
    client = algod.AlgodClient(algod_token, algod_address)

    commit_id = 'abcd1234'

    #print("Signing the transaction")
    signed_txn = vote_repo(client, mnemonic, app_id, url, asset_id, commit_id)
    #print("Transaction signed")

    # Assuming `signed_txn` is your SignedTransaction object
    #print("Type of signed_txn:", type(signed_txn))

    # Convert the signed transaction to a dictionary
    txn_dict = signed_txn.dictify()

    # Serialize the transaction dictionary using msgpack
    serialized_txn = msgpack.packb(txn_dict)

    # Confirm the type to ensure it's bytes
    #print(f"Serialized transaction type: {type(serialized_txn)}")

    # Encode the serialized transaction to base64
    base64_txn = base64.b64encode(serialized_txn).decode('utf-8')

    # Print the base64 encoded transaction
    #print(f"Base64 encoded transaction: {base64_txn}")

    # Print the signed_txn object
    #print("Signed transaction object:", signed_txn)
    #print("Transaction ID:", signed_txn.transaction.get_txid())

    # Encode the signed_txn
    encoded_txn = encoding.msgpack_encode(signed_txn)
    #print("Encoded signed transaction:", encoded_txn)

    # Decode the encoded_txn
    decoded_txn = encoding.msgpack_decode(encoded_txn)
    #print("Decoded transaction object:", decoded_txn)
    #print("Decoded transaction type:", type(decoded_txn))

    ## rename this as it conflicts with lib
    #response = vote_repo(url, commit_id)
    #print(f"Response from vote_repo: {response.text}")  # Print the response text
    #status, parsed_response = parse_vote_repo_response(response)

    #CONFIG = {'url': 'http://localhost:4000/graphql/'}  # Corrected URL

    #"""
    #Makes a POST request to vote for a repo by its URL and commit ID.

    #Args:
    #    url (str): The URL of the repo.
    #    commit_id (str): The commit ID of the repo.

    #Returns:
    #    Dict[str, Any]: The JSON response from the server.
    #"""
    #endpoint = CONFIG['url']

    #query = {
    #    'query': f'''
    #    {{
    #        setVote(
    #            owner: "test_user_name",
    #            repo: "test_user_name/test_repo_name",
    #            defaultHash: "{commit_id}",
    #            childDefaultHash: "{commit_id}",
    #            mergeable: true,
    #            contributor_id: "contributor_id_placeholder",
    #            side: "side_placeholder",
    #            token: "token_placeholder"
    #        )
    #    }}
    #    '''
    #}

    #print(f"vote_repo called with url: {url}, commit_id: {commit_id}")  # Print the input arguments

    #response = requests.post(endpoint, json=query, headers={'accept': 'json'})

    #status, parsed_response = parse_vote_repo_response(response)


    #if status == 'error':
    #    sys.stderr.write(parsed_response + "\n")
    #    sys.exit(1)
    #else:
    #    print(parsed_response)

def main():
    cli()

if __name__ == '__main__':
    main()
