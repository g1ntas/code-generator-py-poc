from accio.commands.base import BaseCommand
from accio.commands.repo import Repo
from accio.commands.run import Run
from accio.commands.list import List


class Root(BaseCommand):
    def setup(self):
        self.add_command(Repo)
        self.add_command(Run)
        self.add_command(List)

    def run(self, args):
        pass
