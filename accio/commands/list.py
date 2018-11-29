from accio.commands.base import BaseCommand


class List(BaseCommand):
    name = "list"
    help = "List all existing generators"

    def setup(self):
        pass

    def run(self, args):
        print(f"Listing...")
