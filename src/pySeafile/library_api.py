
"""A wrapper around the library API using a repo token."""

import tomllib
import requests
import datetime

from dataclasses import dataclass
from .utils import to_datetime
from .items import LibraryItem

from typing import List

TOML_FILE_REQUIRED_SETTINGS = ['server_url', 'library_token']


@dataclass
class LibraryInfo:
    uuid: str
    name: str
    size: int
    file_count: int
    last_modified: datetime.datetime

    @property
    def seconds_since_last_modified(self):
        """Return the number of seconds since this library was last modified"""
        return (datetime.datetime.now(self.last_modified.tzinfo) - \
            self.last_modified).total_seconds()



class Library:
    """A library repo wrapper."""

    def __init__(self, server_url: str, library_token: str):
        self._url = server_url
        self._token = library_token

        self._session = requests.Session()
        self._session.headers.update({'Authorization': f'Token {self._token}'})

    @classmethod
    def from_toml_config(cls, path):
        """Load the server URL and Token from a TOML file."""

        with open(path, 'rb') as f:
            config = tomllib.load(f)

        for pref in TOML_FILE_REQUIRED_SETTINGS:
            if pref not in config:
                raise ValueError(f'"{pref}" setting not found in TOML file')

        return cls(config['server_url'], config['library_token'])

    def get(self, endpoint: str, url_params: dict = None):
        """Perform a GET request on the server."""

        return self._session.get(f'{self._url}{endpoint}', 
                                 params=url_params or {})

    def server_online(self):
        """Return true if the server is online"""
        
        return self.get('/api2/ping/').json() == 'pong'

    def _info_dict(self):
        """Return the raw repo info dict"""
        return self.get('/api/v2.1/via-repo-token/repo-info/').json()

    def info(self) -> LibraryInfo:
        """Return the library info wrapper class"""

        d = self._info_dict()
        last_mod = to_datetime(d.get('last_modified'))

        return LibraryInfo(
            uuid = d.get('repo_id'),
            name = d.get('repo_name'),
            size = d.get('size'),
            file_count = d.get('file_count'),
            last_modified = last_mod,
        )

    def list(self, path, files_only=False, directories_only=False,
             recursive=False, thumbnails=False, thumb_size=48) -> List[LibraryItem]:
        """List all items in the library at the given path."""

        d = list_query_dict(path, files_only, directories_only,
             recursive, thumbnails, thumb_size)

        resp = self.get('/api/v2.1/via-repo-token/dir/', d)
        items = resp.json().get('dirent_list', [])
        return [LibraryItem.from_list_dict(self, d) for d in items]

    def download_link(self, path):
        """Obtain a download link to a file."""

        resp = self.get('/api/v2.1/via-repo-token/download-link/',
                        {'path': path})
        return resp.json()

    def download(self, url, path_on_disk, chunk_size=8192, timeout=10):
        """Download the file, writing it to a path on disk."""

        # todo: allow setting the range header, and appending to file

        resp = self._session.get(url, stream=True, timeout=timeout)

        if resp.status_code == 416:
            # the range request was invalid, file download couldn't be resumed.
            raise RuntimeError('Range header out of range')

        with open(path_on_disk, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if len(chunk) > 0:  # filter out keep-alive chunks
                    f.write(chunk)


def list_query_dict(path, files_only, directories_only,
                    recursive, thumbnails, thumb_size):
    """Build the query dictionary for listing files"""

    d = dict()

    d['path'] = path

    # type
    if files_only and directories_only:
        raise ValueError('cannot have both files only and directories only')
    elif files_only:
        d['type'] = 'f'
    elif directories_only:
        d['type'] = 'd'

    if recursive:
        d['recursive'] = '1'

    if thumbnails:
        d['with_thumbnail'] = 'true'
        d['thumbnail_size'] = thumb_size

    return d
