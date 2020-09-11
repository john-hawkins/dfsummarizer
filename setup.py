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

with open("markdown_test.md", "rb") as f:
    example = f.read().decode("utf-8")

long_descr = long_descr + "\n" + example

setup(
    name = "dfsummarizer",
    packages = ["dfsummarizer"],
    license = "MIT",
    install_requires = ['pandas>=0.25.3', 'numpy>=1.16.4'],
    entry_points = {
        "console_scripts": ['dfsummarizer = dfsummarizer.dfsummarizer:main']
    },
    include_package_data=True,
    version = version,
    description = "Python command line application to summarize a CSV or TSV dataset.",
    long_description = long_descr,
    long_description_content_type='text/markdown',
    author = "John Hawkins",
    author_email = "hawkins.john.c@gmail.com",
    url = "http://john-hawkins.github.io",
    project_urls = {
        'Documentation': "http://john-hawkins.github.io",
        'Source': "https://github.com/john-hawkins/dfsummarizer",
        'Tracker': "https://github.com/john-hawkins/dfsummarizer/issues" 
      }
    )

