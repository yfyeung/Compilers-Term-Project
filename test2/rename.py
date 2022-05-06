
import os

file_list = os.listdir()
file_list.remove('rename.py')
newfile_list = []
for filename in file_list:
    oldfilename = filename
    filename = filename.replace('txt', 'sql')
    os.rename(oldfilename, filename)
