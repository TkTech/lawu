#!/usr/bin/env python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name="jawa",
    packages=find_packages(),
    version="1.0",
    description="Doing fun stuff with JVM ClassFiles.",
    author="Tyler Kennedy",
    author_email="tk@tkte.ch",
    url="http://github.com/TkTech/Jawa",
    keywords=["java", "disassembly", "disassembler"],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Disassemblers"
    ],
    tests_require=[
        'pytest'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'sphinx',
            'sphinxcontrib-googleanalytics',
            'sphinx_rtd_theme',
            'ghp-import'
        ]
    }
)
