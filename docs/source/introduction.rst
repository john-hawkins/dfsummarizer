Introduction
============

``dfsummarizer`` is a Python package which aims to provide an easy and intuitive way 
for summarizing the columns of a dataframe. It will deal natively with data sets larger
than available memory by processing a file in chunks. It will generate a set of standard
statistics for numerical variables, and calculate similar statistics for dates, and 
look at the length of text variables.


Motivation
**********

Data frame summarization is a standard task in data science and the default options in
the python ecosystem provide only partial functionality.

The goal of the package is both a command line app to generate a markdown (or latex) table
summary of a dataset. In addition, a library with a set of re-usable functions that can
be integrated into other apps.


Limitations
***********

- Currently calculates the summary over the entire dataset: TODO: Sample based summary.

- Currently the number of unique values for large data sets is estimated using the Flajolet Martin algorithm. This is suboptimal for low cardinality columns. TODO: Implement a hybrid version that tracks absolute numbers until the cardinality exceeds a defined threshold.


