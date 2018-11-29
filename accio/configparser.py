import re

import yaml

from accio.errors import GeneratorConfigError
from accio.models.generator import Generator
from accio.models.prompt import Prompt


def parse_from_path(path: str) -> Generator:
    with open(path, 'rb') as f:
        return parse(f.read())


def parse(content: bytes) -> Generator:
    config = yaml.load(content)
    _validate_config(config)
    generator = _create_generator(config)
    for name, data in config["prompts"].items():
        prompt = _create_prompt(name, data)
        generator.add_prompt(prompt)
    return generator


def _validate_config(config: dict):
    """
    Validates configuration

    Config consists of following properties:
    config["name"] (string|required):
        Name of the generator used as identifier.

        Name format rules:
        - can contain letters, numbers, dashes and colons;
        - must start with letter;
        - must end with either letter or number
        - can't contain two or more colons or dashes in a row

    config["description"] (string|required):
        Short description (up to 120 characters) of command used to list all available generators.

    config["prompts"] (map|optional):
        Map that contains definitions of variables that will be prompted when generator is ran.

        config["prompts"]["__var_name__"]["type"] (string|required):
            Type of the prompt.

        config["prompts"]["__var_name__"]["question"] (string|required):
            Question that will be showed for prompt.

        config["prompts"]["__var_name__"]["description"] (string|optional):
            Description used for help text.

    :param config: dictionary of yaml parsed config
    :raise GeneratorConfigError: in case config is invalid
    :return: None
    """
    # todo: improve error messages to be more helpful
    if "name" not in config:
        raise GeneratorConfigError("Required property \"name\" not found in config file \"accio.yaml\"")

    if "description" not in config:
        raise GeneratorConfigError("Required property \"description\" not found in config file \"accio.yaml\"")

    if not isinstance(config["name"], str):
        raise GeneratorConfigError("Config property \"name\" must be string")

    if not isinstance(config["description"], str):
        raise GeneratorConfigError("Config property \"description\" must be string")

    if re.match(r"[a-z]+([\-:]?[a-z0-9]+)+", config["name"], re.I) is None:
        raise GeneratorConfigError("Config property \"name\" contains invalid characters or format")

    if len(config["description"]) > 120:
        raise GeneratorConfigError("Config property \"description\" can not be longer than 120 characters")

    if "prompts" in config:
        if not isinstance(config["prompts"], dict):
            raise GeneratorConfigError("Config property \"prompt\" must be map")
        for name, data in config["prompts"].items():
            _validate_prompt(data)


def _validate_prompt(data: dict):
    """
    Validate config structure of single prompt


    :param data:
    :return:
    """
    # todo: validate that type (data["type"]) is set and is valid/existing
    # todo: validate that type (data["question"]) is set and is valid/existing
    # todo: validate that type (data["description"]) is string, if set
    pass


def _create_generator(config):
    generator = Generator()
    generator.name = config["name"]  # todo: validate name to not contain spaces and other invalid chars. Make lowercase
    generator.description = config["description"]  # todo: validate is string
    return generator


def _create_prompt(name, data):
    prompt = Prompt()
    prompt.type = data["type"]
    prompt.variable = name
    prompt.message = data["message"]
    return prompt
