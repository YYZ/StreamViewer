#!/usr/bin/env python

# fixindent.py - Fix indenting in python files by expanding/contracting tabs
# Copyright (C) 2006 Dan Noe / isomerica.net
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, US

#
# $Id$
#

import getopt, sys, re, fileinput

def main():
    try:
        options, remaining = getopt.getopt(sys.argv[1:], "hvts:")
    except getopt.GetoptError:
        usage()
        sys.exit(1)
    verbose = False
    spaces = "4"
    spacestotab = False

    for field, value in options:
        if field  == "-h":
            usage()
            sys.exit()
        if field == "-v":
            verbose = True
        if field == "-t":
            spacestotab = True
        if field == "-s":
            try:
                spaces = int(value)
            except ValueError:
                print "-s Spaces argument must be an integer"
                usage()
                sys.exit()
    
    if len(remaining) == 0:
        process(sys.stdin, spaces, spacestotab, verbose)
    else:
        process(remaining[0], spaces, spacestotab, verbose)

def process(input, spaces, spacestotab, verbose):
    p = re.compile(r"^(\s+)(.*)$")
    for line in fileinput.input(input):
        fixed = False
        if line == "\n":
            sys.stdout.write(line)
            continue
        m = p.match(line)
        if m:
            whitespace = m.group(1)
            if spacestotab:
                newwhitespace = whitespace.replace(" " * spaces, '\t')
                if newwhitespace != whitespace:
                    fixed = True
            else:
                newwhitespace = whitespace.expandtabs(int(spaces))
                if newwhitespace != whitespace:
                    fixed = True
            output = newwhitespace + m.group(2) + "\n"
            if verbose and fixed:
                sys.stderr.write("Fixed: " + output)
            sys.stdout.write(output)
        else:
            sys.stdout.write(line)

def usage():
    print """fixindent.py - Fix indenting in python files by expanding/contracting tabs

Usage:

fixindent.py -hvts <spaces> <inputfile>

Options:
  -h   Help (you are reading it)
  -v   Verbose output
  -t   Convert spaces to tabs
  -s <spaces> Number of spaces to expand/contract

  If <inputfile> is omitted, stdin is used.

fixindent.py version 0.1, Copyright (C) 2007 Dan Noe / isomerica.net
"""

if __name__ == "__main__":
    main()
