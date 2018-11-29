from accio.commands.base import BaseCommand
from accio.commands.repo_add import RepoAdd
from accio.commands.repo_list import RepoList
from accio.commands.repo_remove import RepoRemove
from accio.commands.repo_sync import RepoSync


class Repo(BaseCommand):
    name = "repo"

    def setup(self):
        self.add_command(RepoAdd)
        self.add_command(RepoSync)
        self.add_command(RepoRemove)
        self.add_command(RepoList)

    def run(self, args):
        pass
