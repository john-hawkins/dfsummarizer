# -*- coding: utf-8 -*-

import pandas as pd 
import numpy as np
import math
import os

from .config import max_filesize
from .FlajoletMartin import FMEstimator
 
"""
    dfsummarizer.funcs: Core functions of the dfsummarizer package.
        analyse_df( pandas_dataframe): return a sumamry dataframe of the input dataframe
        analyse_df_in_chunks(path_to_dataset): Read the dataset in chunks and provide a summary
"""


########################################################################################
def analyse_df(df):
    """
        Given a pandas dataframe that is already in memory we generate a table of summary
        statistics and descriptors.
    """
    colnames = df.columns
    records = len(df)
    df = coerce_dates(df)
    rez = pd.DataFrame(columns=('Name', 'Type', 'Unique', 'Nulls', 'Min', 'Mean', 'Max'))

    for name in colnames:
        nacount = len(df[df[name].isna()])
        napercent = round(100*nacount/records,1)
        uniques = df[name].unique().tolist()
        if np.nan in uniques :
            uniques.remove(np.nan)
        unicount = len(uniques)
        unipercent = round(100*unicount/records,1)

        valtype = infer_type(str(type(df.loc[1,name])), unicount, uniques)

        if (valtype == "Char") :
            lenvec = df[name].apply(lambda x: len_or_null(x))
            themin = round(lenvec.min(),3) # "-"
            themean = round(lenvec.mean(),3) #"-"
            themax = round(lenvec.max(),3) #"-"
        elif (valtype == "Bool") :
            newvec = df[name].apply(lambda x: booleanize(x))
            themin = round(newvec.min(),3)
            themean = round(newvec.mean(),3)
            themax = round(newvec.max(),3)
        else:
            if (valtype != "Date") :
                themin = round(df[name].min(),3)
                themean = round(df[name].mean(),3)
                themax = round(df[name].max(),3)
            else :
                themin = str(df[name].min())[0:10]
                themean = str(df[name].mean())[0:10] #"-"
                themax = str(df[name].max())[0:10]

        values_to_add = {
            'Name':name, 
            'Type':valtype,
            'Unique':unipercent, 
            'Nulls':napercent, 
            'Min':themin, 
            'Mean': themean, 
            'Max':themax
        }
        rez = rez.append(values_to_add, ignore_index=True)

    return rez

########################################################################################
def analyse_df_in_chunks(path_to_file):
    """
        Given a path to a large dataset we will iteratively load it in chunks and build
        out the statistics necessary to summarise the whole dataset.
    """
    fsize = os.stat(path_to_file).st_size
    sample_prop = max_filesize / fsize 
    line_count = count_lines(path_to_file)
    chunks = round(line_count * sample_prop)
    temp = {}
    data_iterator = pd.read_csv(path_to_file, chunksize=chunks, low_memory=False)
    total_chunks = 0
    for index, chunk in enumerate(data_iterator, start=0):
        startpoint = 0 + (index*chunks)
        total_chunks = index + 1
        temp = update_temp_summary(temp, chunk, startpoint)
    summary = generate_final_summary(temp, total_chunks)
    return summary

########################################################################################
def generate_final_summary(temp, total_chunks):
    rez = pd.DataFrame(columns=('Name', 'Type', 'Unique', 'Nulls', 'Min', 'Mean', 'Max'))
    for name in temp.keys():
        col = temp[name]
        total = col['nulls'] + col['nonnulls']
        unicount = col['uniques'].estimate()
        if unicount > total:
            uniprop = 1.0
        else:
            uniprop = unicount / total
        #uniprop = col['uniques']/total_chunks
        unipercent = round(100 * uniprop, 1)
        napercent = round((100 * col['nulls']) / total, 1)
        themean = col['sum'] / total
        values_to_add = {
            'Name':name, 
            'Type': col['type'],
            'Unique':unipercent,
            'Nulls':napercent,
            'Min': col['min'],
            'Mean': themean, 
            'Max': col['max']
        }
        rez = rez.append(values_to_add, ignore_index=True)
    return rez

########################################################################################
def update_temp_summary(temp, df, startpoint):
    colnames = df.columns
    records = len(df)
    df = coerce_dates(df)
    for name in colnames:
        if name in temp:
            rez = temp[name]
        else: 
            rez = { "type":[], "sum":0, 
                    "min":np.nan, "max":np.nan, 
                    "uniques":FMEstimator(), "nulls":0, 
                    "nonnulls":0
                   }
        nacount = len(df[df[name].isna()])
        nonnulls = len(df) - nacount
        uniques = df[name].unique().tolist()
        if np.nan in uniques :
            uniques.remove(np.nan)
        unicount = len(uniques)
        uniprop = unicount / len(df)
        valtype = infer_type(str(type(df.loc[startpoint,name])), unicount, uniques)
        if (valtype == "Char") :
            lenvec = df[name].apply(lambda x: len_or_null(x))
            themin = round(lenvec.min(),3) # "-"
            thesum = round(lenvec.sum(),3) #"-"
            themax = round(lenvec.max(),3) #"-"
        elif (valtype == "Bool") :
            newvec = df[name].apply(lambda x: booleanize(x))
            themin = round(newvec.min(),3)
            thesum = round(newvec.sum(),3)
            themax = round(newvec.max(),3)
        else:
            if (valtype != "Date") :
                themin = round(df[name].min(),3)
                thesum = round(df[name].sum(),3)
                themax = round(df[name].max(),3)
            else :
                themin = str(df[name].min())[0:10]
                thesum = str(df[name].sum())
                themax = str(df[name].max())[0:10] 

        rez['type'] = valtype
        rez['sum'] = rez['sum'] + thesum
        rez['nulls'] = rez['nulls'] + nacount
        if isNaN( rez['min'] ) or themin < rez['min']:
            rez['min'] = themin
        if isNaN( rez['max'] ) or themax > rez['max']:
            rez['max'] = themax
        rez['uniques'].update_all(uniques)
        #rez['uniques'] += uniprop
        rez['nonnulls'] = rez['nonnulls'] + nonnulls
        temp[name] = rez
    return temp

########################################################################################
def extract_file_extension(path_to_file):
    return os.path.splitext(path_to_file)[1]

########################################################################################
def load_complete_dataframe(path_to_file):
    """
        We load the entire dataset into memory, using the file extension to determine
        the expected format. We are using encoding='latin1' because it ppears to 
        permit loading of the largest variety of files.
        Representation of strings may not be perfect, but is not important for generating a
        summarization of the entire dataset.
    """
    extension = extract_file_extension(path_to_file).lower()
    if extension == ".csv":
        df = pd.read_csv(path_to_file, encoding='latin1', low_memory=False)
        return df
    if extension == ".tsv":
        df = pd.read_csv(path_to_file, encoding='latin1', sep='\t', low_memory=False)
        return df
    if extension == ".xls" or extension == ".xlsx" or extension == ".odf" :
        df = pd.read_excel(path_to_file)
        return df

    raise ValueError("Unsupported File Type")

########################################################################################
def infer_type(thetype, unicount, uniques):
     valtype = "Char"
     if thetype == "<class 'numpy.float64'>" :
        valtype = "Float"
     if thetype == "<class 'numpy.int64'>" :
        valtype = "Int"
     if thetype == "<class 'pandas._libs.tslib.Timestamp'>" :
        valtype = "Date"
     if thetype == "<class 'pandas._libs.tslibs.timestamps.Timestamp'>" :
        valtype = "Date"
     # Infer Booleans by 2 unique values and additional criteria
     if unicount == 2:
        if (valtype == "Char") :
            temp = [x.lower() for x in uniques]
            temp.sort()
            if (temp == ['no', 'yes']):
                valtype = "Bool"
            if (temp == ['n', 'y']):
                valtype = "Bool"
            if (temp == ['false', 'true']):
                valtype = "Bool"
            if (temp == ['f', 't']):
                valtype = "Bool"
     return valtype

########################################################################################
def count_lines(path_to_file):
    """
    Return a count of total lines in a file. In a way that filesize is irrelevant
    """
    count = 0
    for line in open(path_to_file): count += 1
    return count

########################################################################################
def len_or_null(val):
    """ 
       Alternative len function that will simply return numpy.NA for invalid values 
       This is need to get sensible results when running len over a column that may contain nulls
    """
    try:
        return len(val)
    except:
        return np.nan

########################################################################################
def isNaN(num):
    return num != num

########################################################################################
def booleanize(x):
    if isNaN(x) :
        return x
    else :
        x = x.lower()
    if x == "yes" or x == "y" or x == "true" or x == "t" or x == 1:
        return 1
    else :
        return 0

########################################################################################
def coerce_dates(df):
    return df.apply(
        lambda col: pd.to_datetime(col, errors='ignore')
        if col.dtypes == object
        else col,
        axis=0
    )


########################################################################################
def print_latex(summary):
    print("\\begin{table}[h!]")
    print(" \\begin{center}")
    print("   \\caption{Data Summary Table}")
    print("   \\label{tab:table1}")
    print("   \\begin{tabular}{l|l|r|r|r|r} ")
    print("    \\textbf{Name} & \\textbf{Type} & \\textbf{Unique \%} & \\textbf{Nulls \%} & \\textbf{Min} & \\textbf{Mean} & \\textbf{Max}\\\\")
    print("      \\hline")
    for i in range(len(summary)):
        print("      ", summary.loc[i,"Name"], 
              "&", summary.loc[i,"Type"], 
              "&", summary.loc[i,"Unique"], "%" 
              "&", summary.loc[i,"Nulls"], "%" 
              "&", summary.loc[i,"Min"], 
              "&", summary.loc[i,"Mean"], 
              "&", summary.loc[i,"Max"], "\\\\")
    print("    \\end{tabular}")
    print("  \\end{center}")
    print("\\end{table}")

########################################################################################
def get_spaces(spacer):
    rez = ""
    for i in range(spacer):
        rez = rez + " "
    return rez

########################################################################################
def get_type_spacer(t):
    if (t == "Int") :
        return "    "
    if (t == "Char") :
        return "   "
    if (t == "Date") :
        return "   "
    if (t == "Float") :
        return "  "
    return "   "

########################################################################################
def get_percent_spacer(p):
    if (p==100.0):
       return " "
    elif (p>=10): 
        return "  " 
    else: 
        return "   "

########################################################################################
def get_padded_number(n):
    if (n == "-"):
        return "     -     "
    if (str(n).replace('.','',1).replace('-','',1).isdigit()):
        if (n<0):
            adjus = -1
        else:
            adjus = 0
        if (abs(n)<10):
            return get_spaces(8 - after_decimal(n) + adjus) + str(n) + " "
        if (abs(n)<100):
            return get_spaces(7 - after_decimal(n) + adjus) + str(n)+ " "
        if (abs(n)<1000):
            return get_spaces(6 - after_decimal(n) + adjus) + str(n)+ " "
        if (abs(n)<10000):
            return get_spaces(5 - after_decimal(n) + adjus) + str(n)+ " "
        if (abs(n)<100000):
            return get_spaces(4 - after_decimal(n) + adjus) + str(n)+ " "
        if (abs(n)<1000000):
            return get_spaces(3 - after_decimal(n) + adjus) + str(n)+ " "
        if (abs(n)<10000000):
            return get_spaces(2 - after_decimal(n) + adjus) + str(n)+ " "
    else:
        return str(n) + " "

########################################################################################
def after_decimal(n):
    arr = str(n).split(".")
    if( len(arr)==2 ):
        return len(arr[1])
    else:
        return -1

########################################################################################
def print_markdown(s):
    longest_name = max(s["Name"].apply(lambda x: len_or_null(x)))
    if(longest_name>4):
        name_spacer = longest_name+2
    else:
        name_spacer = 6

    print("| Name ", get_spaces(name_spacer-6), 
        "| Type   | Unique  | Nulls   |  Min       |  Mean      |  Max       |", sep="")
    print("| ---- ", get_spaces(name_spacer-6), 
        "| ------ | ------- | ------- |  ---       |  ----      |  ---       |", sep="")
    for i in range(len(s)):
        print("| ", s.loc[i,"Name"], 
            get_spaces(name_spacer - len(s.loc[i,"Name"]) - 1 ), 
            "| ", s.loc[i,"Type"], get_type_spacer(s.loc[i,"Type"]),
            "| ", get_percent_spacer(s.loc[i,"Unique"]), s.loc[i,"Unique"],"% ", 
            "| ", get_percent_spacer(s.loc[i,"Nulls"]), s.loc[i,"Nulls"],"% ", 
            "| ", get_padded_number(s.loc[i,"Min"]), 
            "| ", get_padded_number(s.loc[i,"Mean"]),
            "| ", get_padded_number(s.loc[i,"Max"]), "|", sep="")


########################################################################################
def round_down(n, decimals=0):
    """
    Round down a number to a specifed number of decimal places
    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier) / multiplier

