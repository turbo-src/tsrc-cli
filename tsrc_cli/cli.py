import sys
import click
from .lib.create_user import create_user
from .lib.create_user import parse_create_user_response
from .lib.get_user import get_user, parse_get_user_response
from .lib.get_tsrcid import get_tsrcid
from .lib.get_tsrckey import get_tsrckey
from .lib.utilities.tx_utility import AlgorandAccount
#from lib.utilities.wallet_utility import (
#    WalletUtility
#)

@click.group()
def cli():
    pass

@cli.group(name="user")
def user():
    pass

@user.command(name="create")
#@click.option('--contributor-id', '-i', help='Contributor ID', required=False)
@click.argument('contributor-name')
@click.option('--contributor-mnemonic', '-m', help='Contributor mnemonic', required=False)
def create_user_cmd(contributor_name, contributor_mnemonic):
    # If contributor_id or contributor_mnemonic isn't passed, get them from the config file
    #if not contributor_id:
    #    contributor_id = get_tsrcid()
    #    if contributor_id is None:
    #        sys.stderr.write("Error: Contributor ID is required.\n")
    #        sys.exit(1)

    #if not contributor_mnemonic:
    #    contributor_mnemonic = get_tsrckey()
    #    if contributor_mnemonic is None:
    #        sys.stderr.write("Error: Contributor mnemonic is required.\n")
    #        sys.exit(1)

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
@click.argument('contributor-id', required=False)
@click.option('--contributor-mnemonic', '-m', help='Contributor mnemonic', required=False)
def get_user_cmd(contributor_id, contributor_mnemonic):
    response = get_user(contributor_id)
    status, parsed_response = parse_get_user_response(response)

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

def main():
    cli()

if __name__ == '__main__':
    main()


