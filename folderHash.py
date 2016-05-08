import sys
import fnmatch
import os
import hashlib
import datetime
import re
import socket

def strip_path(base, path, filename):
    stripped = os.path.join(path, filename)
    stripped = os.path.relpath(stripped, start=base)
    stripped = os.path.normpath(stripped)
    stripped = stripped.replace(os.path.sep, '/')
    return stripped

def md5_hash(pathtofile):
    hasher = hashlib.md5()
    with open(pathtofile, 'rb') as filetohash:
        while True:
            data=filetohash.read(3*1024*1024)
            if not data: break
            hasher.update(data)
    return hasher.hexdigest()

def build_output_file_name(input_folder):
    list = [socket.gethostname()]

    (drive, basepath) = os.path.splitdrive(input_folder)

    if drive:
        list.append(drive.replace(':', ''))

    if basepath:
        if basepath[0] == os.path.sep:
            basepath = basepath[1:]
        list.append(basepath.replace(os.path.sep, '_'))

    return '_'.join(list) + '.txt'

includes = ['*.*'] # for files only
excludes = ['@eaDir'] # for dirs and files

# transform glob patterns to regular expressions
includes = r'|'.join([fnmatch.translate(x) for x in includes])
excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

base = sys.argv[1]

outputfilename = build_output_file_name(base)

with open(outputfilename, mode='w', encoding='utf8', newline='\n') as outputfile:
    begin_time = datetime.datetime.now()
    outputfile.write(begin_time.strftime("%Y%m%d%H%M%S\n"))
    for path, dirnames, filenames in os.walk(base):
        dirnames[:] = [d for d in dirnames if not re.match(excludes, d)]
        dirnames.sort()
        filenames = [f for f in filenames if not re.match(excludes, f)]
        filenames = [f for f in filenames if re.match(includes, f)]
        filenames.sort()
        for filename in fnmatch.filter(filenames, '*.*'):
            outputfile.write(strip_path(base, path, filename) + ' ' + md5_hash(os.path.join(path, filename)) + '\n')
    end_time = datetime.datetime.now()
    outputfile.write(end_time.strftime("%Y%m%d%H%M%S\n"))
    processing_time = end_time - begin_time
    outputfile.write(str(processing_time))
