#!/usr/bin/env python3

"""pySeafile is an easy backup tool using the minimal "repo" token."""

import pathlib

__version__ = '0.1.0'
__author__ = 'kevoc'

from pip._internal.req import parse_requirements
from setuptools import setup, find_packages


MY_DIR = pathlib.Path(__file__).parent.resolve()

# parse the requirements.txt file, generating a list of all
# packages needed for this tool
REQUIREMENTS = list([str(ir.requirement) for ir in
                     parse_requirements('requirements.txt', session=False)])

# Get the long description from the README file
long_description = (MY_DIR / 'README.md').read_text(encoding='utf-8')


setup(
    name='pySeafile',
    version=__version__,
    description=__doc__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kevoc/pySeafile',
    author=__author__,

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords=['seafile', 'backup'],

    package_dir={'pySeafile': 'src/pySeafile'},
    python_requires='>=3.10, <4',
    install_requires=REQUIREMENTS
)
