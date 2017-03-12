#/usr/bin/python3.4
# -*- coding: utf-8 -*-

from os.path import isfile, join, exists, splitext, basename, dirname
from os import mkdir, rename, listdir, remove, rmdir
from shutil import copyfile, rmtree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir_from", help="Directory to rename files in",
                    type=str)
parser.add_argument("ext", help="Initial extension (starting with dot)",
                    type=str)
parser.add_argument("ext_new", help="New extension (starting with dot)",
                    type=str)
args = parser.parse_args()

if not exists(args.dir_from):
    print("Path does not exist: ", args.dir_from)

files = [join(args.dir_from, f) for f in listdir(args.dir_from)
         if isfile(join(args.dir_from, f)) and splitext(f)[1] == args.ext]

for f in files:
    new_name = splitext(basename(f))[0] + args.ext_new
    rename(f, join(dirname(f), new_name))
