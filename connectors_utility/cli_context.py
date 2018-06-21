import os
import click
import pickle


class Context(object):
    """ Context object for CLI
    """
    def __init__(self):
        self.home = os.getcwd()
        self._ensure_directory(os.path.expanduser('~/.data_connectors'))
        self.config = os.path.expanduser('~/.data_connectors/configs.ser')
        self.cache = {}

        if self.config and os.path.isfile(self.config):
            self._deserialize()

    def _serialize(self):
        pickle.dump(self.cache, open(self.config, "wb"))

    def _deserialize(self):
        data = pickle.load(open(self.config, "rb"))
        self.cache.update(data)

    def put(self, namespace, **kwargs):
        space = self.cache.get(namespace) or {}
        space.update(kwargs)
        self.cache[namespace] = space
        self._serialize()

    def get(self, namespace, key):
        space = self.cache.get(namespace) or {}
        return space.get(key)

    def _ensure_directory(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)


pass_context = click.make_pass_decorator(Context, ensure=True)
