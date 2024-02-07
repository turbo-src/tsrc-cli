import sys
import click
from .lib.create_user import create_user  # Adjust the import as necessary
from .lib.create_user import parse_create_user_response  # Adjust the import as necessary
from .lib.get_user import get_user, parse_get_user_response

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


