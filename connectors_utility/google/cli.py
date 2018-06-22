import os
import click
import json
import csv
from connectors_utility.cli_context import pass_context
from connectors_utility.helpers import get_stdin_list
from . import auth

NAMESPACE = __name__


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('--verbose', '-v', is_flag=True, help='Print output verbose')
@pass_context
def cli(ctx, verbose):
    pass


@cli.command()
@pass_context
@click.argument('client-secret-file')
def init(ctx, client_secret_file):
    """ Invoke authentication workflow and get a the access token
    """
    ctx.put_file(NAMESPACE, 'client_secret_file', client_secret_file)
    creds = auth.get_credentials('credentials.json', client_secret_file)
    ctx.put_file(NAMESPACE, 'credentials_file', 'credentials.json')
    os.remove('credentials.json')
    click.echo(creds.to_json())


@cli.command('get')
@pass_context
@click.argument('sheets-id')
@click.argument('values-range')
def sheets_get(ctx, sheets_id, values_range):
    """ Invoke authentication workflow and get a the access token
    """
    creds = auth.get_credentials(
        ctx.get(NAMESPACE, key='credentials_file'),
        ctx.get(NAMESPACE, key='client_secret_file'))

    service = auth.get_service(creds, service='sheets')\
        .spreadsheets()

    results = service.values().get(spreadsheetId=sheets_id, range=values_range).execute()
    click.echo(json.dumps(results))


@cli.command('update')
@pass_context
@click.argument('sheets-id')
@click.argument('values-range')
def sheets_update(ctx, sheets_id, values_range):
    """ Update sheets range with input data
    """
    assert sheets_id, values_range
    service = auth.get_service(ctx.get(NAMESPACE, key='credentials_file'), service='sheets')\
        .spreadsheets()
    values = get_stdin_list()

    body = {
        'values': values
    }

    results = service.values().update(
        spreadsheetId=sheets_id,
        range=values_range,
        valueInputOption="RAW",
        body=body).execute()

    click.echo(json.dumps(results))


@cli.command('show')
@click.argument('key')
@pass_context
def show(ctx, key):
    """ Show the configuration property
    """
    click.echo(ctx.get(NAMESPACE, key))


@cli.command()
@pass_context
def test(ctx):
    """ Invoke authentication workflow and get a the access token
    """
    pass


def main():

    # auth.get_credentials('credentials.json', 'client_secret.json')
    cli()
    pass


if __name__ == "__main__":
    cli()
