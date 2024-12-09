#!/usr/bin/env python3

"""Tests for the Library Class"""

import os
import random
import hashlib
import datetime
import tempfile

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

	def test_directory_list(self):
		"""Ensure directory listings of the library work as expected"""

		lib = Library.from_toml_config(LIBRARY_FILE)
		contents = lib.list('/')

		self.assertGreater(len(contents), 0)

		random_dir = random.choice([i for i in contents if i.is_directory])
		sub_contents = random_dir.get_children()
		self.assertGreater(len(sub_contents), 0)

	def test_downloading(self):
		"""Ensure the download link endpoint is functioning."""

		lib = Library.from_toml_config(LIBRARY_FILE)

		# get a download link
		my_link = lib.download_link('/_Latex/GSWLaTeX.pdf')

		# make a writable temp file for the download
		tmp_path = os.path.join(tempfile.mkdtemp(), 'test.file')

		# download the file.
		lib.download(my_link, tmp_path)

		sha1 = hashlib.sha1()

		with open(tmp_path, 'rb') as f:
			sha1.update(f.read())

		self.assertEqual(sha1.hexdigest(), '2b27fec60e8c78b60df6a942e0f34c5488c804ea')
		breakpoint()

