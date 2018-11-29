import contextlib
import os
import pickle


# 1. stores config file
# 2. stores repo files under subdirectory
from accio import settings


def add(key: str, data: any):
    path = _format_path(key)
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, 'wb') as file:
        pickle.dump(data, file)


def get(key: str, default: any = None):
    path = _format_path(key)

    try:
        with open(path, 'rb') as f:
            content = pickle.load(f)
    except FileNotFoundError:
        content = default

    return content


def remove(key: str):
    path = _format_path(key)

    with contextlib.suppress(FileNotFoundError):
        os.remove(path)


def _format_path(key: str):
    return os.path.join(settings.APP_DIR, key + ".pickle")
