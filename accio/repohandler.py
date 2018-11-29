import os
from urllib.parse import urlparse

from git import Repo

from accio import cache, settings, configparser
from accio.errors import GeneratorConfigError
from accio.models.repository import Repository

CONFIG_FILENAME = "accio.yaml"


def save_repository(repo: Repository):
    """
    Save repository into the cache stacking up with already existing repositories

    :param repo: instance of Repository model
    :return: None
    """
    repositories = cache.get("generators", {})
    repositories[repo.url] = repo
    cache.add("generators", repositories)


def clone_repository(url: str) -> str:
    """
    Clone repository from given URL into app dir

    :param url: valid git url, see http://www.kernel.org/pub/software/scm/git/docs/git-clone.html#URLS
    :return: path to the directory of cloned repository
    """
    repo_dir = _parse_repo_dir(url)
    Repo.clone_from(url, repo_dir)
    return repo_dir


def pull_repository(repo: Repository):
    """
    Pull changes from git repository for given Repository instance

    :param repo: instance of Repository pointing to valid git repository
    :return: path to the directory of cloned repository
    """
    origin = Repo(repo.directory).remote()  # todo: handle exceptions: can throw ValueError
    origin.pull()


def parse_repository(repo_dir: str, url: str) -> Repository:
    """
    Creates Repository model containing all generators parsed from given directory of repository

    It walks over all root level directories looking for config file, then validates each of it
    and saves configuration into Repository model.

    :param repo_dir: local path to the repository's directory
    :param url: valid git repository url
    :raise GeneratorConfigError: in case config was not found or is invalid for one of the generators
    :return: instance of created Repository
    """
    # todo: also parse config from repo root, so repository can be as single generator
    repository = Repository(url, repo_dir)
    for root, dirs, files in os.walk(repo_dir):
        if root == repo_dir:
            dirs.remove(".git")
            continue
        dirs.clear()  # config should be on root level of generator, so don't walk any deeper
        if CONFIG_FILENAME not in files:
            raise GeneratorConfigError("Config file 'accio.yaml' not found in generator's root directory")
        config_path = os.path.join(root, CONFIG_FILENAME)
        generator = configparser.parse_from_path(config_path)
        generator.directory = root
        repository.add_generator(generator)
    return repository


def _parse_repo_dir(url: str) -> str:
    result = urlparse(url)
    path_parts = result.path.split("/")
    directory = os.path.join(settings.APP_DIR, "repos", result.netloc, *path_parts)
    return directory
