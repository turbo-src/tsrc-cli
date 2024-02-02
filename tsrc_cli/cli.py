import click
from .lib.create_user import create_user  # Adjust the import as necessary
from .lib.create_user import parse_create_user_response  # Adjust the import as necessary
from .lib.get_user import get_user, parse_get_user_response

@click.group()
def cli():
    pass

@cli.command(name="create-user")
@click.argument('contributor_id')
@click.argument('contributor_name')
@click.argument('contributor_password')
def create_user_cmd(contributor_id, contributor_name, contributor_password):
    response = create_user(contributor_id, contributor_name, contributor_password)
    parsed_response = parse_create_user_response(response)
    print(parsed_response)

@cli.command(name="get-user")
@click.argument('contributor_id')
def get_user_cmd(contributor_id):
    response = get_user(contributor_id)
    parsed_response = parse_get_user_response(response)
    print(parsed_response)

def main():
    cli()

if __name__ == '__main__':
    main()
