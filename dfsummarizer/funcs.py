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
        napercent = round(100*nacount/records,1)
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
                themean = "-"
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
    print("    \\textbf{Name} & \\textbf{Type} & \\textbf{Missing \%} & \\textbf{Min} & \\textbf{Mean} & \\textbf{Max}\\\\")
    print("      \\hline")
    for i in range(len(summary)):
        print("      ", summary.loc[i,"Name"], 
              "&", summary.loc[i,"Type"], 
              "&", summary.loc[i,"Nulls"], "%" 
              "&", summary.loc[i,"Min"], 
              "&", summary.loc[i,"Mean"], 
              "&", summary.loc[i,"Max"], "\\\\")
    print("    \\end{tabular}")
    print("  \\end{center}")
    print("\\end{table}")

def get_spaces(spacer):
    rez = ""
    for i in range(spacer):
        rez = rez + " "
    return rez

def get_type_spacer(t):
    if (t == "int") :
        return "    "
    if (t == "Char") :
        return "   "
    if (t == "Date") :
        return "   "
    if (t == "Float") :
        return "  "
 
def get_percent_spacer(p):
    if (p<10): 
        return " " 
    else: 
        return ""

def get_padded_number(n):
    if (n == "-"):
        return "     -     "
    if (str(n).replace('.','',1).isdigit()):
        if (n<10):
            return str(n) + "        "
        if (n<100):
            return str(n) + "       "
        if (n<1000):
            return str(n) + "      "
        if (n<10000):
            return str(n) + "     "
        if (n<100000):
            return str(n) + "    "
        if (n<1000000):
            return str(n) + "   "
        if (n<10000000):
            return str(n) + "  "
    else:
        return str(n) + " "

def print_markdown(s):
    longest_name = max(s["Name"].apply(lambda x: len_or_null(x)))
    if(longest_name>4):
        name_spacer = longest_name+2
    else:
        name_spacer = 6

    print("| Name ", get_spaces(name_spacer-6), 
        "| Type   | Missing |  Min       |  Mean      |  Max        |", sep="")
    print("| ---- ", get_spaces(name_spacer-6), 
        "| ------ | ------- |  ---       |  ----      |  ---        |", sep="")
    for i in range(len(s)):
        print("| ", s.loc[i,"Name"], 
            get_spaces(name_spacer - len(s.loc[i,"Name"]) - 1 ), 
            "| ", s.loc[i,"Type"], get_type_spacer(s.loc[i,"Type"]),
            "| ", get_percent_spacer(s.loc[i,"Nulls"]), s.loc[i,"Nulls"],"%   ", 
            "| ", get_padded_number(s.loc[i,"Min"]), 
            "| ", get_padded_number(s.loc[i,"Mean"]),
            "| ", get_padded_number(s.loc[i,"Max"]), " |", sep="")
