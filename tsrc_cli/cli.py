import sys
import click
from .lib.create_user import create_user
from .lib.create_user import parse_create_user_response
from .lib.get_user import get_user, parse_get_user_response
from .lib.get_tsrcid import get_tsrcid
from .lib.get_tsrckey import get_tsrckey

@click.group()
def cli():
    pass

@cli.group(name="user")
def user():
    pass

@user.command(name="create")
@click.option('--contributor-id', '-i', help='Contributor ID', required=False)
@click.argument('contributor-name')
@click.option('--contributor-password', '-p', help='Contributor password', required=False)
def create_user_cmd(contributor_name, contributor_id, contributor_password):
    # If contributor_id or contributor_password isn't passed, get them from the config file
    if not contributor_id:
        contributor_id = get_tsrcid()
        if contributor_id is None:
            sys.stderr.write("Error: Contributor ID is required.\n")
            sys.exit(1)

    if not contributor_password:
        contributor_password = get_tsrckey()
        if contributor_password is None:
            sys.stderr.write("Error: Contributor password is required.\n")
            sys.exit(1)

    response = create_user(contributor_id, contributor_name, contributor_password)
    status, parsed_response = parse_create_user_response(response)

    if status == 'error':
        sys.stderr.write(parsed_response + "\n")
        sys.exit(1)
    else:
        print(parsed_response)

@user.command(name="get")
@click.argument('contributor-id', required=False)
@click.option('--contributor-password', '-p', help='Contributor password', required=False)
def get_user_cmd(contributor_id, contributor_password):
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


