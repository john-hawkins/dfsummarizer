import numpy as np
from dfsummarizer.funcs import isNaN
from dfsummarizer.funcs import len_or_null
from dfsummarizer.funcs import extract_file_extension

def test_my_sum():
    assert 2 + 3 == 5, "math works"

def test_extract_file_extension():
    assert extract_file_extension("./README.md") == ".md"

def test_isNaN():
    assert isNaN(0) == False
    assert isNaN(np.nan) == True

def test_len_or_null():
    assert len_or_null("the") == 3
    assert np.isnan(len_or_null(np.nan)) == True

