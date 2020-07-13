# -*- coding: utf-8 -*-
 
"""setup.py: setuptools control."""
 
import re
from setuptools import setup
 
version = re.search(
        '^__version__\s*=\s*"(.*)"',
        open('dfsummarizer/dfsummarizer.py').read(),
        re.M
    ).group(1)
 
with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name = "dfsummarizer",
    packages = ["dfsummarizer"],
    install_requires=[
        'pandas','numpy'
    ],
    entry_points = {
        "console_scripts": ['dfsummarizer = dfsummarizer.dfsummarizer:main']
        },
    version = version,
    description = "Python command line application to summarize a CSV or TSV dataset.",
    long_description = long_descr,
    long_description_content_type='text/markdown',
    author = "John Hawkins",
    author_email = "hawkins.john.c@gmail.com",
    url = "http://john-hawkins.github.io",
    )

