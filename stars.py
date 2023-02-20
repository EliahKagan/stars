# Copyright (c) 2023 Eliah Kagan
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

"""Query a GitHub user's starred repositories and their topics."""

__all__ = ['get_starred_repos', 'extract_topics']

import collections
from collections.abc import Sequence, Mapping
import datetime
import itertools
import json
import logging
import operator
from typing import Any

import requests

_REQUEST_TIMEOUT = datetime.timedelta(minutes=2)
"""The maximum time we wait for any single request to complete."""


def _typename(obj: object) -> str:
    """Get the name of the type that obj is a direct instance of."""
    return type(obj).__name__


def _ensure_isinstance(obj: object, cls: type) -> None:
    """Raise TypeError if object is not an instance of cls."""
    if not isinstance(obj, cls):
        raise TypeError(
            f'result is {_typename(obj)!r}, expected {_typename(cls)!r}')


def _fetch_starred_repos(user: str) -> list[dict[str, Any]]:
    """Fetch GitHub repositories starred by a user, via the GitHub REST API."""
    repos = []

    for page in itertools.count(1):
        response = requests.get(
            url=f'https://api.github.com/users/{user}/starred?page={page}',
            timeout=_REQUEST_TIMEOUT.total_seconds(),
        )
        response.raise_for_status()
        part = response.json()
        _ensure_isinstance(part, list)

        if not part:
            break

        repos.extend(part)

    return repos


def get_starred_repos(user: str) -> list[dict[str, Any]]:
    """Get GitHub repositories starred by a user, with disk caching."""
    path = f'starred-repos-{user}.json'

    try:
        # Attempt to load a saved result instead of calling the API.
        with open(path, mode='r', encoding='utf-8') as file:
            repos = json.load(file)
    except OSError:
        # They were not saved. Fetch them from the API and save them.
        logging.info('No saved results for %r. Using GitHub API.', user)
        repos = _fetch_starred_repos(user)
        with open(path, mode='w', encoding='utf-8') as file:
            json.dump(obj=repos, fp=file, indent=4)
    else:
        # They were saved. Check that JSON decoded to the correct type.
        logging.info(f'Loaded saved result for {user}.')
        _ensure_isinstance(repos, list)

    return repos


def extract_topics(repos: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    """Group repositories overlappingly by declared topic."""
    topics = collections.defaultdict[str, list](list)

    for repo in sorted(repos, key=operator.itemgetter('full_name')):
        for topic in repo['topics']:
            topics[topic].append(repo['full_name'])

    return dict(topics)
