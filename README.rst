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
 
Additional detail available in the [companion blog post](https://john-hawkins.github.io/posts/2020/07/dfsummarizer-dataframe-summarizer-application/)
 
Built using the [bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)


Testing
*******

You can use this application multiple ways

Use the runner:

    $ ./dfsummarizer-runner.py markdown data/test.csv

Invoke the directory as a package:

    $ python -m dfsummarizer markdown data/test.csv
   
Or simply install the package and use the command line application directly


Installation
************

Installation from the source tree (or via pip from PyPI)::

    $ python setup.py install

Now, the ``dfsummarizer`` command is available::

    $ dfsummarizer md test.csv

This will produce a markdown table summarizing the contents of the CSV
file test.csv. 

