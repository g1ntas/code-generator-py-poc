import os

from accio import cache, generatorhandler
from accio.commands.base import BaseCommand
from accio.errors import Error
from accio.sandbox.context import Context


class Run(BaseCommand):
    name = "run"
    help = "Run specified generator"

    def setup(self):
        self.add_argument("generator", help="Name of the generator")
        self.add_argument("-f", "--force", action="store_true", help="Overwrite existing files without explicit confirmation")
        # self.add_argument("-h, --help", help="Show usage manual for generator")
        # self.add_argument("-w, --working-dir [dir]", help="Specify different working dir than current one")

    def run(self, args):
        # todo: improve prompts:
        #   todo: validate inputs
        repos = self.retrieve_repositories()
        matches = self.find_matching_generators(args.generator, repos)
        generator = self.choose_generator(matches)

        context = Context()
        self.prompt_vars(generator, context)

        replace_file_func = (lambda x: True) if args.force else self.prompt_replace_file
        generatorhandler.run(generator, context, os.getcwd(), self.on_file_create, replace_file_func)

    def on_file_create(self, path: str):
        print(os.path.basename(path))

    def prompt_replace_file(self, path: str) -> bool:
        print(f"File at {path} already exists.\n")
        response = bool(int(input(f"Do you want to replace it? ")))
        return response

    def retrieve_repositories(self):
        repositories = cache.get("generators")
        if repositories is None:
            raise Error(f'no repositories found. Make sure that you added repository with generators first')
        return repositories

    def find_matching_generators(self, name, repos):
        matches = []
        for _, repository in repos.items():
            if name in repository.generators:
                matches.append(repository.generators[name])
        return matches

    def choose_generator(self, generators):
        if len(generators) == 1:
            return generators[0]
        print("Multiple generator matches have been found:")
        for index, generator in generators:
            print("[%d] %s (%s)" % index + 1, generator.name, generator.description)
        index = int(input("Enter which generator would you like to run: "))  # todo: validate that enter number
        if index < 0 or index >= len(generators):
            print("invalid index")
            return self.choose_generator(generators)
        return generators[index]

    def prompt_vars(self, generator, context):
        for prompt in generator.prompts:
            if prompt.type == "input":
                value = input("%s " % prompt.message)
                context.set(prompt.variable, value)
