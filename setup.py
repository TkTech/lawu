#!/usr/bin/env python
# -*- coding: utf8 -*-
from setuptools import setup, find_packages

setup(
    name="jawa",
    packages=find_packages(),
    version="0.1.0",
    description="Doing stuff with JVM classfiles.",
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
    scripts=[
        'scripts/jawa-shell'
    ]
)
