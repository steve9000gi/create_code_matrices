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
import json
import re
import ntpath

def read_cblm(path):
    print 'read_cblm("' + path + '")'

def read_all_cblms(cblm_dir):
    """  Get a list of all the rows in all the CBLMs. """

    print 'read_all_cblms("' + cblm_dir + '")'
    cblm_files = []
    cblm_files += [fn for fn in os.listdir(cblm_dir) if fn.endswith("-CBLM.csv")]
    #print(str(cblm_files), sep = '\n')
    #print "\n".join(cblm_files)
    clist = []
    for i, cblm in enumerate(cblm_files):
        cblm_file = cblm_dir + '/' + cblm
        with open(cblm_file) as cblm: # Read CBLM file as list, each item a row:
             rows = cblm.read().split("\n");

        for row in rows: # clist becomes a list of sublists, each sublist a row
            r = row.split("\t") # Split each row into a list of items
            clist.append(r)
        clist.pop() # get rid of empty last row
    return clist

def create_unique_code_list(cblm_list):
    """ Accepts cblm_list, a list of all the rows in all the CBLMs, and returns
            a list of all the codes from cblm_list.
    """
    code_list = []
    for row in cblm_list:
        code_list.append(row[4])
    return code_list

def write_code_matrices(code_matrix_dir):
    print 'write_code_matrices("' + code_matrix_dir + '")'


# main:
cblm_dir = sys.argv[1]
code_matrix_dir = sys.argv[2]

unique_code_list = sorted(set(create_unique_code_list(read_all_cblms(cblm_dir))))
print "\n".join(unique_code_list)
write_code_matrices(code_matrix_dir)
    

