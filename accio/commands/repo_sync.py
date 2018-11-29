from accio import cache, repohandler
from accio.commands.base import BaseCommand
from accio.errors import Error


class RepoSync(BaseCommand):
    name = "sync"
    help = "Synchronize all repositories with latest changes"

    def setup(self):
        pass

    def run(self, args):
        # todo: improve output
        repos = self.retrieve_repositories()
        for url, repo in repos.items():
            print(f"Pulling changes from {url}...\n")
            repohandler.pull_repository(repo)

    def retrieve_repositories(self):
        # todo: refactor duplicated method (another one in accio.commands.run)
        repositories = cache.get("generators")
        if repositories is None:
            raise Error(f'no repositories found. Make sure that you added repository with generators first')
        return repositories
