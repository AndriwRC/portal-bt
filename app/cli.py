import typer
from sqlmodel import Session

from .database.connection import Connection
from .database.models import *
from .database.seeders.permissions import PermissionSeeder
from .database.seeders.roles import RoleSeeder


app = typer.Typer()


@app.callback()
def main():
    """
    Entry point for the project CLI.

    This command does not execute any action by itself.
    Use one of the available subcommands to perform
    administrative or maintenance tasks.
    """
    pass


@app.command()
def seed():
    """
    Seed base application data into the database.

    This command initializes required system data such as:
    - Base permissions
    - Base roles
    - Role–permission assignments

    The operation is idempotent and can be safely re-run
    without creating duplicated records.
    """

    typer.echo(f"{'-'*20} Manual Seeding Script {'-'*20}")
    typer.echo("Initializing seeding operation...")

    with Session(Connection.ENGINE) as session:
        PermissionSeeder().run(db=session)
        RoleSeeder().run(db=session)

    typer.echo("Seeding completed.")


if __name__ == "__main__":
    app()
