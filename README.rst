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
 
Additional detail available in the `companion blog post <https://john-hawkins.github.io/posts/2020/07/dfsummarizer-dataframe-summarizer-application/>`_ 

Built using the 
`bootstrap cmdline template <https://github.com/jgehrcke/python-cmdline-bootstrap>`_
 by `jgehrcke <https://github.com/jgehrcke>`_


Notes
*****

Initial implementation can handle larger files by chunking data and iteratively
building statistics. All statistics are robust except for estimation of the proportion
of unique values. We have used a simple implementation of the Flajolet Martin algorithm
based on the implemnetation by `Javia Jinkal <https://github.com/javiajinkal/Flajolet-Martin>`_

This `review article by Phillip Gibbons <https://www.cs.cmu.edu/~gibbons/Phillip%20B.%20Gibbons_files/Distinct-Values-Estimation-over-Data-Streams-PBGibbons.pdf>`_ gives a great overview of the alternatives.


Testing
*******

You can use this application multiple ways

Use the runner:

    $ ./dfsummarizer-runner.py markdown data/test.csv > markdown_test.md

Which was used to generate the markdown `output test file <markdown_test.md>`_

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

