#!/usr/bin/env python
import os
import sys
import re
import StringIO
import argparse

"""
Command line replace with python regex and format string.
"""

def s(inp, replace, replacewith): 
    match = re.search(replace, inp)
    matches = []
    named_matches = {}
    if not match:
        return inp
    if match.group(0):
        matches = [match.group(0)]
    if match.groups():
        matches = matches + list(match.groups())
    named_matches = match.groupdict()
    if matches:
        try:
            replacewith = replacewith.format(*matches, **named_matches)
        except:
            pass
        return re.sub(replace, replacewith, inp)
    return inp


def main():
    argp = argparse.ArgumentParser(description="String replace with Python \
                                   regex and format string")
    argp.add_argument("replace")
    argp.add_argument("replacewith")
    argp.add_argument("-f","--file")
    argp.add_argument("-i", "--in-place", action="store_true")
    argp.add_argument("-m", "--mode", choices=["line", "blob"], default="line")
    args = argp.parse_args()

    inf = sys.stdin
    outf = sys.stdout
    filename = args.file
    
    if filename:
        inf = open(filename, "r")
        if in_place:
            outf=StringIO.StringIO()

    if args.mode == "line":
        line = inf.readline()
        while line:
            r = s(line, 
                  args.replace, 
                  args.replacewith)

            outf.write(r)
            line = inf.readline()
    else:
        inp = inf.read()
        outf.write(s(inp, args.replace, args.replacewith))

    if filename and args.in_place:
        with open(filename, "w") as f:
            f.write(outf.getvalue())


if __name__ == "__main__":
    main()