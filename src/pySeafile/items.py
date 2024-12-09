
from __future__ import annotations

import os
import datetime

from .utils import to_datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass


if TYPE_CHECKING:
    from .library_api import Library


@dataclass(frozen=True)
class LibraryItem:
    """A wrapper for a library item."""

    lib: Library
    id: str
    last_modified: datetime.datetime
    name: str
    parent_dir: str
    permission: str
    is_starred: bool
    type: str

    @classmethod
    def from_list_dict(cls, lib_obj: Library, list_dict: dict):
        """Create an item object using the returned dictionary from
        an API directory listing."""

        return cls(lib_obj,
                   id=list_dict.get('id'),
                   last_modified=to_datetime(list_dict.get('mtime')),
                   name=list_dict.get('name'),
                   parent_dir=list_dict.get('parent_dir'),
                   permission=list_dict.get('permission'),
                   is_starred=list_dict.get('starred'),
                   type=list_dict.get('type'))

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.full_path}", type="{self.type}")'

    @property
    def full_path(self):
        return os.path.join(self.parent_dir, self.name)

    @property
    def is_directory(self):
        return self.type == 'dir'

    @property
    def is_file(self):
        return self.type == 'file'  # todo: validate

    def get_children(self, files_only=False, directories_only=False,
                     recursive=False, thumbnails=False, thumb_size=48):
        """Return a list of the contents of this folder."""

        if not self.is_directory:
            raise ValueError('only directories can have children queried')

        return self.lib.list(self.full_path, files_only, directories_only,
                             recursive, thumbnails, thumb_size)

