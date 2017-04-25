#!/usr/bin/env python

""" create_code_matrices
    Usage:
    ./create_code_matrces.py cblm_dir code_matrix_dir
    Assumes that the files in the two directories follow this naming
    convention:
        (cblm) coded binary link matrix: "<name>-CBLM.csv"
        code matrix: "<name>-CM.csv"
    where <name> is a string that may or may not be constructed according to a
    convention defined in
    https://github.com/steve9000gi/extractMaps/blob/master/README.md.
"""

import sys
import os
import csv
import numpy as np
import pandas as pd

def read_cblm(path):
    print 'read_cblm("' + path + '")'

def create_code_list(cblm_dir):
    """  Read in all the CBLM files in cblm_dir, and return a list of all the
         codes.
    """

    print 'create_code_list("' + cblm_dir + '")'
    cblm_files = []
    cblm_files += [fn for fn in os.listdir(cblm_dir) if fn.endswith("-CBLM.csv")]
    clist = []
    for i, cblm in enumerate(cblm_files):
        cblm_file = cblm_dir + '/' + cblm
        with open(cblm_file, "rb") as cblm: 
            reader = csv.reader(cblm, delimiter = '\t')
            next(reader, None)
            for row in reader: 
                clist.append(row[4])
    return clist

def write_code_matrices(code_matrix_dir):
    print 'write_code_matrices("' + code_matrix_dir + '")'

def build_empty_code_matrix(code_list):
    """ Construct 2D square matrix with dimensions = length of code_list
    """
    dim = len(code_list)
    temp = [[0 for x in range(dim)] for y in range(dim)] 

    labels = map(str, range(0, dim))
    return pd.DataFrame(temp, columns=labels, index=labels, dtype=np.int8)

# main:
cblm_dir = sys.argv[1]
code_matrix_dir = sys.argv[2]

unique_code_list = sorted(set(create_code_list(cblm_dir)))
#print "\n".join(unique_code_list)
for i, code in enumerate(unique_code_list):
    print str(i) + ": \"" + code + "\""
empty_code_matrix = build_empty_code_matrix(unique_code_list)
#print(np.matrix(empty_code_matrix))
with pd.option_context('display.max_rows', None, 'display.max_columns', 3):
     print(empty_code_matrix)

empty_code_matrix.to_csv(path_or_buf = code_matrix_dir + "/empty.csv",
    sep = '\t')

"""
for row in empty_code_matrix:
    for val in row:
        print '{:2}'.format(val),
    print
write_code_matrices(code_matrix_dir)
    
"""
