# -*- coding: utf-8 -*-
 
"""dfsummarizer.dfsummarizer: provides entry point main()."""
 
__version__ = "0.1.0"
  
import numpy as np
import pandas as pd
import sys

from .funcs import analyse_df
from .funcs import print_latex
from .funcs import print_markdown
 
 
def main():
    if len(sys.argv) < 2:
        print("ERROR: MISSING ARGUMENTS")
        print_usage(sys.argv)
        exit(1)
    else:
        format = sys.argv[1]
        dataset = sys.argv[2]

        df = pd.read_csv(dataset)
        summary = analyse_df(df)
        if(format=="latex"):
            print_latex(summary)
        elif(format=="markdown"):
            print_markdown(summary)
        else: 
            print(summary)


def print_usage(args):
    """ Command line application usage instrutions. """
    print("USAGE ")
    print(args[0], " <FORMAT: 'simple' or 'latex' or 'markdown'> <PATH TO CSV>")


