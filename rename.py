# /usr/bin/python3.4
# -*- coding: utf-8 -*-

from os.path import isfile, join, exists, splitext, basename
from os import mkdir, rename, listdir, remove, rmdir
from shutil import copyfile, rmtree
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir_from", help="Directory to rename files in",
                    type=str)
parser.add_argument("--dir_to", help="Directory to put renamed files to",
                    type=str)
parser.add_argument("-p", "--pattern", type=str,
                    help="Rename pattern (without extension!). Define inc number as \"%n\"")
parser.add_argument("--unsafe", help="Rename using temporary directory to avoid collisions,"
                                   "if you want to place renamed files to the same directory",
                    action="store_false")
parser.add_argument("-d", "--duplicate", help="Copy files, not move",
                    action="store_true")
args = parser.parse_args()

if not exists(args.dir_from):
    print("Path does not exist: ", args.dir_from)


files = [join(args.dir_from, f) for f in listdir(args.dir_from) if isfile(join(args.dir_from, f))]

using_tmp = False  # We use tmp directory to avoid collisions while renaming

if not args.unsafe and (not args.dir_to or args.dir_from == args.dir_to):
    dir_to = join(args.dir_from, ".tmp_rename")
    if not exists(dir_to):
        mkdir(dir_to)
    using_tmp = True
elif args.dir_to is None:
    dir_to = args.dir_from
else:
    dir_to = args.dir_to
    if not exists(dir_to):
        mkdir(dir_to)

if not args.pattern:
    pattern = [""]
else:
    pattern = args.pattern.split("%n")

pattern = pattern
if not args.duplicate:
    operation = rename
else:
    operation = copyfile

for i in range(len(files)):
    new_name = "".join([j+str(i+1) for j in pattern[:-1]]) + pattern[-1]
    if new_name == "":
        new_name = str(i+1)
    extension = splitext(files[i])[1]
    new_name += extension
    new_name = join(dir_to, new_name)
    operation(files[i], new_name)

if using_tmp:
    files = [join(dir_to, f) for f in listdir(dir_to) if isfile(join(dir_to, f))]
    for f in files:
        operation(f, join(args.dir_from, basename(f)))
    rmtree(dir_to)


