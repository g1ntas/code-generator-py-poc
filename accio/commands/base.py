from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import Type, ClassVar


class BaseCommand:
    name: ClassVar[str] = ""
    help: ClassVar[str] = ""

    def __init__(self, argparser: ArgumentParser):
        self._argparser: ArgumentParser = argparser
        self._subparsers: _SubParsersAction = None
        self._children = []

        self.setup()
        argparser.set_defaults(func=self.run)

    def setup(self):
        raise NotImplementedError("Setup method not implemented")

    def run(self, args: Type[Namespace]):
        raise NotImplementedError("Run method not implemented")

    def add_command(self, command: Type["BaseCommand"]):
        # subparsers = self._argparser.add_subparsers()
        subparsers = self._add_or_get_subparsers()
        parser = subparsers.add_parser(command.name, help=command.help)
        self._add_child(command(parser))

    def add_argument(self, *args, **kwargs):
        self._argparser.add_argument(*args, **kwargs)

    def _add_child(self, command):
        self._children.append(command)

    def _add_or_get_subparsers(self):
        if self._subparsers is None:
            self._subparsers = self._argparser.add_subparsers()
        return self._subparsers
