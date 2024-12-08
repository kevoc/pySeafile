#!/usr/bin/env python3

"""Tests for the Library Class"""

import datetime

from unittest import TestCase

from pySeafile import Library
from pySeafile import path_to_local_file

# "server.toml" contains the URL and token for the server
# you want to test against. It should contain 2 lines, like
# the following:
#		server_url = "https://cloud.seafile.com/"
#		library_token = "abcdef123456abcdef123456abcdef123456abcd"
LIBRARY_FILE = path_to_local_file("server.toml")


class pySeafileLibraryTests(TestCase):
	"""Tests for the pySeafile Library."""

	def test_library_online(self):
		"""Ensure metadata can be requested for the library."""

		lib = Library.from_toml_config(LIBRARY_FILE)
		self.assertTrue(lib.server_online())

	def test_library_info(self):
		"""Ensure metadata can be requested for the library."""

		lib = Library.from_toml_config(LIBRARY_FILE)
		info = lib.info()

		self.assertIsInstance(info.uuid, str)
		self.assertIsInstance(info.name, str)
		self.assertIsInstance(info.size, int)
		self.assertIsInstance(info.file_count, int)
		self.assertIsInstance(info.last_modified, datetime.datetime)

		self.assertGreater(info.seconds_since_last_modified, 0)

