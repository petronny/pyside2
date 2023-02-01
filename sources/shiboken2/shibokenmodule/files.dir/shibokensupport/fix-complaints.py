# This Python file uses the following encoding: utf-8
# It has been edited by fix-complaints.py .

#############################################################################
##
## Copyright (C) 2021 The Qt Company Ltd.
## Contact: https://www.qt.io/licensing/
##
## This file is part of Qt for Python.
##
## $QT_BEGIN_LICENSE:COMM$
##
## Commercial License Usage
## Licensees holding valid commercial Qt licenses may use this file in
## accordance with the commercial license agreement provided with the
## Software or, alternatively, in accordance with the terms contained in
## a written agreement between you and The Qt Company. For licensing terms
## and conditions see https://www.qt.io/terms-conditions. For further
## information use the contact form at https://www.qt.io/contact-us.
##
## $QT_END_LICENSE$
##
#############################################################################

from __future__ import print_function, absolute_import

"""
fix-complaints.py

This module fixes the buildbot messages of external python files.
Run it once after copying a new version. It is idem-potent, unless
you are changing messages (what I did, of course :-) .
"""

import os
import glob

patched_file_patterns = "backport_inspect.py typing27.py python_minilib_*.py"

offending_words = {
    "behavio""ur": "behavior",
    "at""least": "at_least",
    "reali""sed": "realized",
}

utf8_line = "# This Python file uses the following encoding: utf-8\n"
marker_line = "# It has been edited by {} .\n".format(
                  os.path.basename(__file__))

def patch_file(fname):
    with open(fname) as f:
        lines = f.readlines()
    dup = lines[:]
    for idx, line in enumerate(lines):
        for word, repl in offending_words.items():
            if word in line:
                lines[idx] = line.replace(word, repl)
                print("line:{!r} {!r}->{!r}".format(line, word, repl))
    if lines[0].strip() != utf8_line.strip():
        lines[:0] = [utf8_line, "\n"]
    if lines[1] != marker_line:
        lines[1:1] = marker_line
    if lines != dup:
        with open(fname, "w") as f:
            f.write("".join(lines))

def doit():
    dirname = os.path.dirname(__file__)
    patched_files = []
    for name in patched_file_patterns.split():
        pattern = os.path.join(dirname, name)
        patched_files += glob.glob(pattern)
    for fname in patched_files:
        print("Working on", fname)
        patch_file(fname)

if __name__ == "__main__":
    doit()

# end of file
