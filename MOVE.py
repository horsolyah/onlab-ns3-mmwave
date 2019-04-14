#!/usr/bin/python3

import os
from datetime import datetime

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

timestamp = datetime.now().strftime('%y%m%d_%H%M%S')

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
TARGET_PATH = os.path.join(os.path.join(BASE_PATH, 'output'), timestamp)

if not os.path.isdir(TARGET_PATH): os.makedirs(TARGET_PATH)
files = [f for f in os.listdir(BASE_PATH) if os.path.isfile(f)]

for _file in files:
    if _file not in whitelist:
        print('> ' + _file)

print('Will be moved to ./output/' + timestamp + '/')
inp = input('Are you sure? (y/n)')
if inp != 'y': exit(0)

for _file in files:
    if _file not in whitelist:
        file_path = os.path.join(BASE_PATH, _file)
        new_path = os.path.join(TARGET_PATH, _file)
        os.rename(file_path, new_path)
