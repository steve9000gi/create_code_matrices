#!/usr/bin/env python

""" create_code_presence_matrix.py

    Generate a matrix where the column names are the names of all the System
    Support Map files in a project, and the row names are all the "codes" 
    (node text category names) for that project, and each element is the number
    of times a code appears in the corresponding file. 

    Usage:
        create_code_presence_matrix.py cblm_dir output_dir

    Args:
        cblm_dir: A directory of Coded Binary Link Matrix (CBLM) files.
        output_dir: A directory (required to exist) where the code presence
            matrix is going to be put.

    Requires that the files in cblm_dir follow these naming conventions:
        CBLM file: "<name>-CBLM.csv"
    where <name> is a string that may or may not be constructed according to a
    convention defined in
    https://github.com/steve9000gi/extractMaps/blob/master/README.md.
"""

import sys
import os
import csv
import numpy as np
import pandas as pd
from create_code_matrices import get_cblm_file_list, build_cblm_path_list, create_code_list

def main():
    cblm_dir = sys.argv[1]
    code_matrix_dir = sys.argv[2]
    cblm_file_list = get_cblm_file_list(cblm_dir)
    cblm_path_list = build_cblm_path_list(cblm_dir, cblm_file_list)
    code_list = sorted(set(create_code_list(cblm_path_list)))
    
    # print "type(cblm_file_list): " + type(cblm_file_list).__name__
    # print "type(cblm_path_list): " + type(cblm_path_list).__name__
    # print "type(code_list): " + type(code_list).__name__

    print "cblm_file_list: " + str(cblm_file_list)
    print "cblm_path_list: " + str(cblm_path_list)
    print "code_list: " + str(code_list)

if __name__ == "__main__":
    main()

