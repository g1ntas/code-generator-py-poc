from accio.commands.base import BaseCommand
from accio import repohandler


class RepoAdd(BaseCommand):
    name = "add"
    help = "Add new accio git repository"

    def setup(self):
        self.add_argument("url", help="Url to git repository")

    def run(self, args):
        # todo: check if directory already exist
        repo_dir = repohandler.clone_repository(args.url)
        repository = repohandler.parse_repository(repo_dir, args.url)
        repohandler.save_repository(repository)
