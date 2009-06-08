"""
Recursive;y search all .py files for twisted.web2 and replace with
codenode.external.twisted.web2
"""

import os
import sys
import glob
import re

serep = re.compile('(apps\.compress)')
replace = 'compress'



def searchAndReplaceInFile(fname):
    f = file(fname, 'r')
    fr = f.read()
    f.close()
    fixed = serep.sub(replace, fr)

    f = file(fname, 'w')
    f.write(fixed)
    f.close()

def dofix(a, dname, fnames):
    print '%s fnames' % str(len(fnames))
    for f in fnames:
        if f.find('.py') > 0:
            searchAndReplaceInFile(os.path.join(dname, f))

def main(basedir):
    os.path.walk(basedir, dofix, 'a')

if __name__ == '__main__':
    basedir = sys.argv[1]
    main(os.path.abspath(basedir))
