import pandas as pd
import numpy as np
from dfsummarizer.funcs import isNaN
from dfsummarizer.funcs import len_or_null
from dfsummarizer.funcs import extract_file_extension

from dfsummarizer.funcs import analyse_df

def test_extract_file_extension():
    assert extract_file_extension("./README.md") == ".md"
    assert extract_file_extension("./README.text") == ".text"
    assert extract_file_extension("./README.txt") == ".txt"

def test_isNaN():
    assert isNaN(0) == False
    assert isNaN(np.nan) == True

def test_len_or_null():
    assert len_or_null("the") == 3
    assert np.isnan(len_or_null(np.nan)) == True

def test_simple():
    df = pd.DataFrame({'ID':[1,2,3], "text":["First","2nd","Third"], "num":[10,13,10]})
    rez =  analyse_df(df)
    assert rez["Name"][0] == "ID"
    assert rez["Name"][1] == "text"
    assert rez["Unique Vals"][0] == 3
    assert rez["Unique Vals"][1] == 3
    assert rez["Type"][0] == "Int"
    assert rez["Min"][0] == 1
    assert rez["Mean"][0] == 2
    assert rez["Max"][0] == 3
    assert rez["Type"][2] == "Int"
    assert rez["Min"][2] == 10
    assert rez["Mean"][2] == 11
    assert rez["Mode"][2] == 10
    assert rez["Max"][2] == 13

def test_nan_mode():
    df = pd.DataFrame({'ID':[1,2,3,4,5], "num":[3,np.nan,1,np.nan,np.nan]})
    rez =  analyse_df(df)
    #assert rez["Type"][1] == "Int"
    assert rez["Mode"][1] == "NaN"
    assert rez["Mean"][1] == 2.0

