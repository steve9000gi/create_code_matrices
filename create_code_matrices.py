#!/usr/bin/env python

""" create_code_matrices
    Usage:
    ./create_code_matrices.py cblm_dir code_matrix_dir
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

def create_code_list(cblm_files):
    """  Read in all the CBLM files in cblm_dir, and return a list of all the
         codes.
    """
    clist = []
    for cblm in cblm_files:
        with open(cblm, 'rb') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None) # skip headers
            for row in reader:
                clist.append(row[4])
    return clist

def get_cblm_file_list(cblm_dir):
    cblm_files = []
    cblm_files += [fn for fn in os.listdir(cblm_dir) if fn.endswith('-CBLM.csv')]
    return cblm_files

def build_cblm_path_list(cblm_dir, cblm_file_list):
    return [cblm_dir + "/" + filename for filename in cblm_file_list]

def build_cm_path_list(cblm_files, cm_dir):
    cm_files = []
    for cblm_fname in cblm_files:
        if cblm_fname.endswith("-CBLM.csv"):
            cm_path = cm_dir + "/" + cblm_fname[:-7] + "M.csv"
            cm_files.append(cm_path)
        else:
            print "build_cm_file_list: invalid CBLM file name" + cblm_fname
    return cm_files

def initialize_data_frame(code_list):
    """ Construct 2D square data frame with dimensions = length of code_list and
        all elements 0.
    """
    dim = len(code_list)
    temp = np.zeros((dim, dim), dtype=np.int8)
    labels = map(str, range(0, dim))
    return pd.DataFrame(temp, columns=labels, index=labels, dtype=np.int8)

def populate_df(cblm, df_template, master_code_list):
    """ For each row in the cblm, get the code, find out which nodes the current
        node is linked to, find out the codes for each of those, and add 1 to the
        values in the two locations (we're treating edges as non- or bi-
        directional) in the data frame that corresponds to those two codes.
    """
    popd_df = df_template.copy()
    cblm_df = pd.read_csv(cblm, sep='\t')
    curr_code_list = cblm_df["Code"].values.tolist()
    blm = cblm_df.loc[:, '0':]
    for i, row in blm.iterrows():
        rlist = row.values.tolist() # sequential indices, not nodeID col labels
        for j, elt in enumerate(rlist):
            if elt != 0:
                x = master_code_list.index(curr_code_list[j])
                y = master_code_list.index(curr_code_list[i])
                popd_df.iloc[x, y] += 1
                #print "blm[" +  str(i) + ", " + str(j) + "]: <" + str(elt) \
                #    + ">; type: " + type(elt).__name__
    return popd_df

def write_code_matrix(file_path, df, code_list):
    with open(file_path, 'w') as f:
        #f.write('Code ID')
        df.to_csv(path_or_buf=f, sep='\t')
        f.write('\n\nLegend:\nID\tCode\n')
        for i, code in enumerate(code_list):
            f.write(str(i) + '\t"' + code + '"\n')

def write_code_matrices(cblm_paths, cm_paths, df_template, code_list):
    for i, cblm in enumerate(cblm_paths):
        popd_df = populate_df(cblm, df_template, code_list)
        write_code_matrix(cm_paths[i], popd_df, code_list)

def main():
    cblm_dir = sys.argv[1]
    code_matrix_dir = sys.argv[2]
    cblm_file_list = get_cblm_file_list(cblm_dir)
    cblm_path_list = build_cblm_path_list(cblm_dir, cblm_file_list)
    print "*** " + str(len(cblm_path_list)) + " cblm paths: "
    print '\n'.join(cblm_path_list)
    code_list = sorted(set(create_code_list(cblm_path_list)))
    #print '\n'.join(code_list)
    cm_path_list = build_cm_path_list(cblm_file_list, code_matrix_dir)
    df_template = initialize_data_frame(code_list)
    write_code_matrices(cblm_path_list, cm_path_list, df_template, code_list)

if __name__ == "__main__":
    main()
