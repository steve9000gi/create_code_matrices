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

# main:
cblm_dir = sys.argv[1]
code_matrix_dir = sys.argv[2]

unique_code_list = sorted(set(create_code_list(cblm_dir)))
#unique_code_list = create_code_list(cblm_dir)
#print "\n".join(unique_code_list)
for i, code in enumerate(unique_code_list):
    print str(i) + ": \"" + code + "\""
write_code_matrices(code_matrix_dir)
    

