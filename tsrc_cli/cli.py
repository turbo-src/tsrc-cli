import click
from .lib.create_user import create_user  # Adjust the import as necessary

@click.group()
def cli():
    pass

@cli.command(name="create-user")
@click.argument('owner')
@click.argument('repo')
@click.argument('contributor_id')
@click.argument('contributor_name')
@click.argument('contributor_signature')
@click.argument('token')
def create_user_cmd(owner, repo, contributor_id, contributor_name, contributor_signature, token):
    create_user(owner, repo, contributor_id, contributor_name, contributor_signature, token)

def main():
    cli()

if __name__ == '__main__':
    main()
