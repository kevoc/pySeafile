
"""A wrapper around the library API using a repo token."""

import tomllib
import requests
import datetime

from dataclasses import dataclass


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
        
        return self.get('/api2/ping/').text.strip('"') == 'pong'

    def _info_dict(self):
        """Return the raw repo info dict"""
        return self.get('/api/v2.1/via-repo-token/repo-info/').json()

    def info(self) -> LibraryInfo:
        """Return the library info wrapper class"""

        d = self._info_dict()
        last_mod = datetime.datetime.strptime(
            d.get('last_modified'), '%Y-%m-%dT%H:%M:%S%z')

        return LibraryInfo(
            uuid = d.get('repo_id'),
            name = d.get('repo_name'),
            size = d.get('size'),
            file_count = d.get('file_count'),
            last_modified = last_mod,
        )

    def list(self):
        """List all items in the library at the given path."""

