import click
from .lib.create_user import create_user  # Adjust the import as necessary

@click.group()
def cli():
    pass

@cli.command(name="create-user")
def create_user_cmd():
    create_user()  # Replace with the actual function you want to call

def main():
    cli()

if __name__ == '__main__':
    main()
