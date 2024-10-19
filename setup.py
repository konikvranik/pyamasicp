#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(this_dir, "README.rst"), "r") as f:
    long_description = f.read()

PACKAGES = find_packages(exclude=["tests", "tests.*", "build"])

setup(
    name="pyama",
    version="0.1.0",
    author="Petr Vraník",
    author_email="hpa@suteren.net",
    description=(
        "Client for iiyama TV rs232 over lan protocol"
    ),
    license="MIT",
    keywords="rs232 lan iiyama home-assistant",
    url="https://github.com/konikvranik/pyama/",
    packages=PACKAGES,
    install_requires=[],
    long_description=long_description,
    test_suite="tests",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "Topic :: Home Automation",
        "Topic :: Multimedia",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],
    entry_points={
        "console_scripts": [
            "pyama=pyama.__main__:main",
        ],
    },
)
