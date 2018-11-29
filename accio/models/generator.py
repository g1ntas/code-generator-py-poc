from accio.models.template import Template


class Generator:
    def __init__(self):
        self.name = ''
        self.directory = ''
        self.description = ''
        self.prompts = []
        self.templates = []

    def add_template(self, template: Template):
        self.templates.append(template)

    def get_filename(self):
        return 'commands/' + self.name.replace(':', '.')

    def add_prompt(self, prompt):
        self.prompts.append(prompt)
