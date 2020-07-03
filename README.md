dfsummarizer: Dataframe Summarizer
----------------------------------

Simple command line application to create a summary of a dataframe.

This was motivated by the fact that the summary function for a pandas
dataframe ignore all non-numeric columns, and does not contain multiple
common analytical considerations: how many unique values, how many missing
values, min and max dates, min, mean and max string lengths.

Will support both Latex and Markdown output formats.

