#!/usr/bin/env python

""" matrices_to_3cols.py

    Reads in a directory of code matrices. outputs a directory of "3cols," 2D
    arrays, each arranged in three columns, thusly:
    
    from    to   value

    where "from" and "to" are codes, and "value" is the number of edges in the
    originating set of SSMs that go from "from" to "to."

    Usage:
        CMs_to_3cols.py cm_dir output_dir

"""
import sys
import os
import csv
import numpy as np
import pandas as pd


def get_file_list(dir, suffix):
    """ Get a list of all the files in a directory ending in "suffix".

    Arg:
        dir: the path to a directory that contains CBLM files.
        suffix: the ending substring used for selecting files.

    Returns:
        a list of files in dir ending with suffix..
    """

    files = []
    files += [fn for fn in os.listdir(dir) if fn.endswith(suffix)]
    return files


def build_path_list(dir, file_list):
    """ Builds a list of full paths to a set of files.
    """
    return [dir + "/" + filename for filename in file_list]


def build_3col_path_list(cm_files, out_dir):
    """ Builds a list of full paths to a set of 3col files. An error message is
        printed to stdout for any file that doesn't follow the 3col file naming
        convention.

    Args:
       cm_files: A list of CM filenames, used as the basis for creating 3col
           filenames.
       out_dir: Path to a directory into which 3col files are intended to go.

    Returns:
       A list of full paths to 3col files.
    """
    out_files = []
    for cm_fname in cm_files:
        if cm_fname.endswith("-CM.csv"):
            out_path = out_dir + "/" + cm_fname[:-6] + "3col.csv"
            out_files.append(out_path)
        else:
            print "build_3col_path_list: invalid CM file name " + cm_fname
    return out_files



def print_list(list, title):
    i = 0
    width = 3
    print "\n" + title + ":\n"
    for item in list:
        print "%s. %s" % (str(i).rjust(width), item)
        i += 1


def convert_CM_to_3col(cm_path, outfile_path):
    cm = pd.read_csv(cm_path, delimiter="\t", index_col=0)
    outfile = open(outfile_path, "w")
    outfile.write("From:\tTo:\tValue:\n")
    for row_name, row in cm.iterrows():
        for col_name, value in row.iteritems():
            outfile.write(col_name + "\t" + row_name + "\t" + str(value) + "\n")
    outfile.close()


def convert_CMs_to_3cols(cm_paths, out_paths):
    """ Write out a set of 3col files, each of which corresponds to one of the
        CM files represented by a set of paths to CM files. 

    Args:
        cm_paths: A list of the full paths to a set of CM files.
        out_paths: A list of full paths to which 3col files are to be written.

    Returns:
        None
    """
    for i, cm_path in enumerate(cm_paths):
        print "%s: %s\t->\t%s" % (str(i).rjust(3), cm_path, out_paths[i])
        convert_CM_to_3col(cm_path, out_paths[i])


def main():
    cm_dir = sys.argv[1]
    out_dir = sys.argv[2]
    cm_file_list = get_file_list(cm_dir, "-CM.csv")
    cm_path_list = build_path_list(cm_dir, cm_file_list)    
    out_path_list = build_3col_path_list(cm_file_list, out_dir)
    convert_CMs_to_3cols(cm_path_list, out_path_list)


if __name__ == "__main__":
      main()
