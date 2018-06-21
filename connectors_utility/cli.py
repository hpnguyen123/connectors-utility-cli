import click
from .cli_context import pass_context


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@pass_context
def cli(ctx):
    """ CLI Utility to interact with MSGraph API
    """
    click.echo('cli')


@cli.command()
@pass_context
def test(ctx):
    """ Invoke authentication workflow
    """
    click.echo('test')


def main():
    cli()


if __name__ == "__main__":
    cli()
