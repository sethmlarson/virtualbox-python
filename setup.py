#!/usr/bin/env python
from setuptools import setup
import os


base_dir = os.path.dirname(os.path.abspath(__file__))
about = {}
with open(os.path.join(base_dir, "virtualbox", "__about__.py")) as f:
    exec(f.read(), about)


setup(
    name=about["__title__"],
    version=about["__version__"],
    packages=["virtualbox", "virtualbox.library_ext"],
    author=about["__author__"],
    author_email=about["__author_email__"],
    maintainer=about["__maintainer__"],
    maintainer_email=about["__maintainer_email__"],
    url=about["__url__"],
    description="Complete implementation of VirtualBox's COM API with a Pythonic interface",
    long_description=open("README.rst").read(),
    license=about["__license__"],
    zip_safe=False,
    install_requires=[],
    platforms=["cygwin", "win", "linux"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Security",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: System :: Clustering",
        "Topic :: System :: Distributed Computing",
        "Topic :: System :: Emulators",
        "Topic :: Software Development :: Testing",
    ],
    test_suite="tests",
)
