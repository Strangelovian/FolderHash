import sys
import fnmatch
import os
import csv
import hashlib
import base64
import datetime

def strippath(base, path, filename):
    stripped = os.path.join(path, filename)
    stripped = os.path.relpath(stripped, start=base)
    stripped = os.path.normpath(stripped)
    stripped = stripped.replace(os.path.sep, '/')
    return stripped

def base64hash(pathtofile):
    hasher = hashlib.md5()
    with open(pathtofile, 'rb') as filetohash:
        while True:
            data=filetohash.read(3*1024*1024)
            if not data: break
            hasher.update(data)
    return base64.b64encode(hasher.digest()).decode("utf-8")

base = sys.argv[1]
(drive, basepath) = os.path.splitdrive(base)
outputfilename = os.path.normpath(basepath).replace(os.path.sep, '_') + '.csv'
with open(outputfilename, 'w+') as outputfile:
    outputcsv=csv.writer(outputfile, lineterminator="\n")
    for path, dirnames, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, '*.*'):
            outputcsv.writerow([strippath(base, path, filename), base64hash(os.path.join(path, filename))])
