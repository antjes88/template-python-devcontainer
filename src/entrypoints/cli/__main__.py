import click
import warnings
from dotenv import load_dotenv

from src.entrypoints.cli.dummy import dummy

warnings.filterwarnings("ignore", category=UserWarning)


@click.group()
def cli():
    pass


cli.add_command(dummy)

if __name__ == "__main__":
    load_dotenv(dotenv_path=".env", override=True)
    cli()
