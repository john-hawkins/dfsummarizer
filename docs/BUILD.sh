#!/bin/bash

rm ./source/dfsummarizer.rst
rm ./source/modules.rst

make clean
sphinx-apidoc -o ./source ../dfsummarizer
make html

