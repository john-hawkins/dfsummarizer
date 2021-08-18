# -*- coding: utf-8 -*-
 
"""dfsummarizer.dfsummarizer: provides entry point main()."""
 
import numpy as np
import pandas as pd
import sys
import os

from .funcs import load_complete_dataframe
from .funcs import analyse_df
from .funcs import analyse_file
from .funcs import analyse_file_in_chunks
from .funcs import print_latex
from .funcs import print_markdown
from .funcs import print_csv
from .config import max_filesize
 
def main():
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        format = sys.argv[1]
        dataset = sys.argv[2]

        filesize = os.stat(dataset).st_size

        if filesize<max_filesize:
            # df = load_complete_dataframe(dataset)
            # summary = analyse_df(df)
            summary = analyse_file(dataset)
        else:
            summary = analyse_file_in_chunks(dataset)

        if(format=="latex"):
            print_latex(summary)
        elif(format=="markdown"):
            print_markdown(summary)
        elif(format=="csv"):
            print_csv(summary)
        else: 
            print(summary)


def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " <FORMAT> <PATH TO DATASET>")
    print("  <FORMAT> - 'simple' or 'csv' or 'latex' or 'markdown'")
    print("  <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf")
    print("")


