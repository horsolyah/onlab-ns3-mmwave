#!/usr/bin/python3

import os

whitelist = '''.gitattributes
.hgtags
.gitignore
.hgignore
.lock-waf_linux2_build
CLEAN.py
MOVE.py
AUTHORS
CHANGES.html
_clean.py
LICENSE
Makefile
README
RELEASE_NOTES
test.py
testpy.supp
utils.py
utils.pyc
VERSION
waf
waf.bat
wscript
wutils.py
wutils.pyc'''.split('\n')

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(f)]

for _file in files:
    if _file not in whitelist:
        print('X ' + _file)

print('Will be deleted.')
inp = input('Are you sure? (y/n)')
if inp != 'y': exit(0)

for _file in files:
    if _file not in whitelist:
        file_path = os.path.join(BASE_PATH, _file)
        os.remove(file_path)
