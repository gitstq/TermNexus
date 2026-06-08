#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TermNexus - AI Terminal Workspace Intelligence Engine
Setup configuration
"""

from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="termnexus",
    version="1.0.0",
    author="TermNexus Team",
    author_email="termnexus@example.com",
    description="🧠 TermNexus - AI Terminal Workspace Intelligence Engine | AI终端工作区智能引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/TermNexus",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "termnexus=termnexus.cli:main",
            "tnx=termnexus.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
