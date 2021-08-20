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

from dfsummarizer import __version__
 
def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "-v":
            print(" Version:", __version__)
            exit(1)
        elif sys.argv[1] == "-h":
            print_usage(sys.argv)
            exit(1)
        else:
            print("INVALID OPTION: ", sys.argv[1])
            print_usage(sys.argv)
            exit(1)
    elif len(sys.argv) < 3:
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
    print(" USAGE ")
    print(" ", args[0], " [OPTIONS] <FORMAT> <PATH TO DATASET>")
    print("   <FORMAT>          - 'simple' or 'csv' or 'latex' or 'markdown'")
    print("   <PATH TO DATASET> - Supported file types: csv, tsv, xls, xlsx, odf")
    print("   [OPTIONS]")
    print("      -v             - Print version")
    print("      -h             - Print this usage help")
    print("")


