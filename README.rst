dfsummarizer
===========

This is a data frame summarizing application designed to work as either a function
library or a command line application. It will accept a CSV or TSV file and 
produce a table summarizing all columns individually.

This was motivated by the fact that the summary function for a pandas
data frame ignores all non-numeric columns, and does not contain multiple
common analytical considerations: how many unique values, how many missing
values, min and max dates, min, mean and max string lengths.

Output can be generated as either Latex or Markdown.

Released and distributed via setuptools/PyPI/pip for Python 2 and 3.
 
Additional detail available in the article:
http://john-hawkins.github.io/dfsummarizer-dataset-summarizer-application/

   
Installation
************

Installation from the source tree (or via pip from PyPI)::

    $ python setup.py install

Now, the ``dfsummarizer`` command is available::

    $ dfsummarizer md test.csv

This will produce a markdown table summarizing the contents of the CSV
file test.csv. 

