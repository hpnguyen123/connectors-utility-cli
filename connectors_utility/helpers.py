import click
import json


def get_stdin_list():
    """ Get std input as a list
    """
    results = []
    raw = click.get_text_stream('stdin').read()
    if raw:
        data = json.loads(raw)
        if isinstance(data, (list, tuple)):
            results = data
        else:
            results.append(data)

    return results
