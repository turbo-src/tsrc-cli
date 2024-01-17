import click
from .lib.create_user import create_user  # Adjust the import as necessary
from .lib.create_user import parse_create_user_response  # Adjust the import as necessary

@click.group()
def cli():
    pass

@cli.command(name="create-user")
@click.argument('contributor_id')
@click.argument('contributor_name')
@click.argument('contributor_signature')
@click.argument('token')
def create_user_cmd(contributor_id, contributor_name, contributor_signature, token):
    response = create_user(contributor_id, contributor_name, contributor_signature, token)
    parsed_response = parse_create_user_response(response)
    print(parsed_response)

def main():
    cli()

if __name__ == '__main__':
    main()
