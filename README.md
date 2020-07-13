dfsummarizer
============

This is an application to summarize the variables in a data frame.
It will accept a CSV, TSV or XLS file and produce a table summarizing 
all columns individually.

This was motivated by the fact that the summary function for a pandas
data frame ignores all non-numeric columns, and does not contain multiple
common analytical considerations: how many unique values, how many missing
values, min and max dates, min, mean and max string lengths.

Output can be generated as either Latex or Markdown.

Released and distributed via setuptools/PyPI/pip for Python 3.
 
Additional detail available in the [companion blog post](https://john-hawkins.github.io/posts/2020/07/dfsummarizer-dataframe-summarizer-application/)

Built using the 
[bootstrap cmdline template](https://github.com/jgehrcke/python-cmdline-bootstrap)
 by [jgehrcke](https://github.com/jgehrcke)


## Notes


Initial implementation can handle larger files by chunking data and iteratively
building statistics. All statistics are robust except for estimation of the proportion
of unique values. We have used a simple implementation of the Flajolet Martin algorithm
based on the implementation by [Javia Jinkal](https://github.com/javiajinkal/Flajolet-Martin)

This [review article by Phillip Gibbons](https://www.cs.cmu.edu/~gibbons/Phillip%20B.%20Gibbons_files/Distinct-Values-Estimation-over-Data-Streams-PBGibbons.pdf) gives a great overview of the alternatives.


## Testing

You can use this application multiple ways

Use the runner:

```
./dfsummarizer-runner.py markdown data/test.csv > markdown_test.md
```

Which was used to generate the markdown [output test file](markdown_test.md)

Invoke the directory as a package:

```
python -m dfsummarizer markdown data/test.csv
```

Or simply install the package and use the command line application directly


# Installation

Installation from the source tree (or via pip from PyPI)::

```
python setup.py install
```

Now, the ``dfsummarizer`` command is available::

```
dfsummarizer markdown test.csv
```

This will produce a markdown table summarizing the contents of the CSV
file test.csv

