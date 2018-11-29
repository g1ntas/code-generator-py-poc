from accio.commands.base import BaseCommand


class RepoList(BaseCommand):
    name = "list"
    help = "List all existing repositories"

    def setup(self):
        pass

    def run(self, args):
        print(f"Listing...")
