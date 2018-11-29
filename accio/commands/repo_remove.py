from accio.commands.base import BaseCommand


class RepoRemove(BaseCommand):
    name = "remove"
    help = "Remove existing repository with it's all generators"

    def setup(self):
        self.add_argument("index", help="Index of repository to remove")
        # self.add_argument("--all", help="Remove all repositories")
        # self.add_argument("-f, --force", help="Force remove and don't ask for confirmation")

    def run(self, args):
        print(f"Removing: {args.index}")
