#!/usr/bin/env python
from setuptools import setup

import re
import platform
import os
import sys


install_requires = []

tests_require = ['begins', 'funconf']


def load_version(filename='./virtualbox/version.py'):
    """Parse a __version__ number from a source file"""
    with open(filename) as source:
        text = source.read()
        match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", text)
        if not match:
            msg = "Unable to find version number in {}".format(filename)
            raise RuntimeError(msg)
        version = match.group(1)
        return version


setup(
    name="pyvbox",
    version=load_version(),
    packages=["virtualbox",
              "virtualbox.library_ext"],
    author="Michael Dorman",
    author_email="mjdorma+pyvbox@gmail.com",
    url="https://github.com/mjdorma/pyvbox",
    description="A complete VirtualBox Main API implementation",
    long_description=open('README.rst').read(),
    license="Apache-2.0",
    zip_safe=False,
    install_requires=install_requires,
    platforms=['cygwin', 'win', 'linux'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Microsoft',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Security',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: System :: Clustering',
        'Topic :: System :: Distributed Computing',
        'Topic :: System :: Emulators',
        'Topic :: Software Development :: Testing'
    ],
    test_suite="tests",
    tests_require=tests_require
)
