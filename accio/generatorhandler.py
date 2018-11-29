import os
from typing import Callable

from accio import repohandler, tplengine
from accio.models.generator import Generator
from accio.sandbox.context import Context

TEMPLATE_EXTENSION = ".accio"


def run(generator: Generator,
        context: Context,
        working_dir: str,
        on_create: Callable[[str], None]=(lambda x: None),
        replace_if_exists: Callable[[str], bool]=(lambda x: False)
        ):
    """
    Process generator to parse and generate all template files at current working directory

    :param generator: instance of Generator
    :param context: instance of Context applied for generator's sandbox environment
    :param working_dir: Directory where files will be generated
    :param on_create: Callback applied after each file is created
    :param replace_if_exists: Callback applied for each file path. It decides if existing file will be replaced or not.
        By default all already existing files are ignored.

    :return: None
    """

    for root, dirs, files in os.walk(generator.directory):
        if root == generator.directory:
            files.remove(repohandler.CONFIG_FILENAME)
            continue

        # raise GeneratorConfigError((root, dirs, files))
        for filename in files:
            # todo: make a copy of context for each file so data won't be shared between
            abspath = os.path.join(root, filename)
            # todo: refactor path manipulation
            dirname = _get_relative_working_dir(abspath, generator.directory, working_dir)
            filename = os.path.basename(abspath)
            if _is_dynamic_template(filename):
                filename = filename[:-6]
            context.filename = filename
            file_content = _render_file(abspath, context)
            # todo: validate if filename from context is valid
            # todo: convert / and \ slashes by current system to support cross platforms
            dest = os.path.join(dirname, context.filename)
            _create_missing_dirs(dest)
            # todo: maybe possible to implement yield generator
            if os.path.exists(dest) and replace_if_exists(dest) is False:
                continue

            with open(dest, 'w') as file:
                file.write(file_content)
                on_create(dest)


def _is_dynamic_template(path: str) -> bool:
    return path[-6:] == TEMPLATE_EXTENSION


def _create_missing_dirs(path: str):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def _render_file(path: str, context: Context) -> str:
    with open(path, 'r') as f:
        if _is_dynamic_template(path):
            return tplengine.render(f.read(), context)
        return f.read()


def _get_relative_working_dir(abspath: str, start_dir: str, working_dir: str) -> str:
    relpath = os.path.relpath(abspath, start_dir)  # make relative to start_dir
    relpath = os.path.join(working_dir, relpath)  # make relative to working_dir
    return os.path.dirname(relpath)
