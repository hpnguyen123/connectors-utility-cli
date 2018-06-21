""" CLI Utility to interact with MSGraph API
"""
import click
import json
from . import auth
from connectors_utility.cli_context import pass_context

NAMESPACE = __name__


def get_request_session(ctx):
    client_id = ctx.get(NAMESPACE, 'client_id')
    tokens = ctx.get(NAMESPACE, 'tokens')

    tokens = auth.ensure_tokens(client_id, tokens)
    ctx.put(NAMESPACE, tokens=tokens)
    return auth.get_request_session(tokens)


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@pass_context
def cli(ctx):

    """ Gets the current session.  If token expired, refresh token
    """
    pass


@cli.command()
@pass_context
@click.argument('client-id')
def init(ctx, client_id):
    """ Invoke authentication workflow
    """
    tokens = auth.acquire_token_with_device_code(client_id, auto=True)
    ctx.put(NAMESPACE, client_id=client_id)
    ctx.put(NAMESPACE, tokens=tokens)


@cli.command()
@pass_context
@click.argument('api', required=True)
def get(ctx, api):
    """ Invoke get api
    """
    api = auth.api_endpoint(api)
    session = get_request_session(ctx)
    response = session.get(api)
    click.echo(response.text)


@cli.command()
@pass_context
@click.argument('api', required=True)
def put(ctx, api):
    """ Invoke put api
    """
    session = get_request_session(ctx)
    api = auth.api_endpoint(api)
    data = click.get_text_stream('stdin').read()
    response = session.put(api, headers={'Content-Type': 'text/plain'}, data=data )
    click.echo(response.text)


def main():
    cli()


if __name__ == "__main__":
    cli()
