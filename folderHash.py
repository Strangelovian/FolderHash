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

def md5hash(pathtofile):
    hasher = hashlib.md5()
    with open(pathtofile, 'rb') as filetohash:
        while True:
            data=filetohash.read(3*1024*1024)
            if not data: break
            hasher.update(data)
    return hasher.hexdigest()

base = sys.argv[1]
(drive, basepath) = os.path.splitdrive(base)
outputfilename = os.path.normpath(basepath).replace(os.path.sep, '_') + '.txt'
with open(outputfilename, 'w+') as outputfile:
    begin_time = datetime.datetime.now()
    outputfile.write(begin_time.strftime("%Y%m%d%H%M%S\n"))
    for path, dirnames, filenames in os.walk(base):
        dirnames.sort()
        for filename in fnmatch.filter(filenames, '*.*'):
            outputfile.write(md5hash(os.path.join(path, filename)) + ' ' + strippath(base, path, filename) + '\n')
    end_time = datetime.datetime.now()
    outputfile.write(end_time.strftime("%Y%m%d%H%M%S\n"))
    processing_time = end_time - begin_time
    outputfile.write(str(processing_time))
with open(outputfilename + '.md5', 'w+') as md5checksumfile:
    md5checksumfile.write(md5hash(outputfilename) + '\n')
