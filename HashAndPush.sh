#!/bin/sh
cd ~
FOLDER="/volume1/photo/2015/2015_07_18"
python3 folderHash.py $FOLDER
mv *.csv src/FolderHashes
cd src/FolderHashes
git fetch
git rebase
git add -A
git commit -m "new hash file for folder $FOLDER"
git push
cd ~
