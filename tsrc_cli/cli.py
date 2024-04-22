import sys
import click
from .lib.create_user import create_user
from .lib.create_user import parse_create_user_response
from .lib.get_user import get_user, parse_get_user_response
from .lib.get_user_by_name import get_user_by_name, parse_get_user_by_name_response
from .lib.create_repo import parse_create_repo_response
from .lib.get_tsrcid import get_tsrcid
from .lib.get_tsrckey import get_tsrckey
from .lib.utilities.tx_utility import AlgorandAccount
from .lib.blockchain.blockchain import create_repo

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
    if not contributor_mnemonic:
        sys.stderr.write("Error: Contributor mnemonic is required.\n")
        sys.exit(1)

    # Create an instance of AlgorandAccount for the new account (user) with the provided mnemonic
    account = AlgorandAccount(mnemonic_phrase=contributor_mnemonic)
    contributor_id = account.address

    # Sign the transaction using the create_repo function from blockchain.py
    signed_txn = create_repo(account)

    response = requests.post(
        CONFIG['url'],
        json={
            'query': f'''
            {{
                createRepo(contributor_id: "{contributor_id}", repo_name: "{contributor_name}", contributor_password: "{signed_txn}") {{
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

    status, parsed_response = parse_create_repo_response(response)

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

def main():
    cli()

if __name__ == '__main__':
    main()
