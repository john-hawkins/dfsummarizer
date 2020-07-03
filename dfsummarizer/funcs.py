# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np
 
"""dfsummarizer.funcs: functions within the dfsummarizer package."""


def analyse_df(df):
    colnames = df.columns
    records = len(df)
    df = coerce_dates(df)
    rez = pd.DataFrame(columns=('Name', 'Type', 'Nulls', 'Min', 'Mean', 'Max'))

    for name in colnames:
        nacount = len(df[df[name].isna()])
        napercent = round(100*nacount/records,3)
        valtype = "Char"
        thetype = str(type(df.loc[1,name]))
        if thetype == "<class 'numpy.float64'>" :
           valtype = "Float"
        if thetype == "<class 'numpy.int64'>" :
           valtype = "Int"
        if thetype == "<class 'pandas._libs.tslib.Timestamp'>" :
           valtype = "Date"
        if thetype == "<class 'pandas._libs.tslibs.timestamps.Timestamp'>" :
           valtype = "Date"
        if (valtype == "Char") :
            lenvec = df[name].apply(lambda x: len_or_null(x))
            themin = "-"
            themean = "-"
            themax = "-"
        else:
            if (valtype != "Date") :
                themin = round(df[name].min(),3)
                themean = round(df[name].mean(),3)
                themax = round(df[name].max(),3)
            else :
                themin = str(df[name].min())[0:10]
                themean = '-'
                themax = str(df[name].max())[0:10]

        values_to_add = {
            'Name':name, 
            'Type':valtype, 
            'Nulls':napercent, 
            'Min':themin, 
            'Mean': themean, 
            'Max':themax
        }
        rez = rez.append(values_to_add, ignore_index=True)

    return rez

def len_or_null(val):
    """ Alternative len function that will simply return numpy.NA for invalid values """
    try:
        return len(val)
    except:
        return np.nan

def coerce_dates(df):
    return df.apply(
        lambda col: pd.to_datetime(col, errors='ignore')
        if col.dtypes == object
        else col,
        axis=0
    )


def print_latex(summary):
    print("\\begin{table}[h!]")
    print(" \\begin{center}")
    print("   \\caption{Data Summary Table}")
    print("   \\label{tab:table1}")
    print("   \\begin{tabular}{l|l|r|r|r|r} ")
    print("    \\textbf{Col Name} & \\textbf{Type} & \\textbf{Missing \%} & \\textbf{Min} & \\textbf{Mean} & \\textbf{Max}\\\\")
    print("      \\hline")
    for i in range(len(summary)):
        print("      ", summary.loc[i,"Name"], 
              "&", summary.loc[i,"Type"], 
              "&", summary.loc[i,"Nulls"], 
              "&", summary.loc[i,"Min"], 
              "&", summary.loc[i,"Mean"], 
              "&", summary.loc[i,"Max"], "\\\\")
    print("    \\end{tabular}")
    print("  \\end{center}")
    print("\\end{table}")

def print_markdown(summary):
    print(summary)


