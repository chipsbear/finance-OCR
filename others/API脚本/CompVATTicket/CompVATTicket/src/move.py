import os
import shutil
rootdir_data="./primitive_answer/"
rootdir_tested="./cache/tested/"
rootdir_dst="./scanprimitive_answer/"
for parent,dirnames,filenames in os.walk(rootdir_data):
    for filename in filenames:
        if(filename[0]=='X'):
            shutil.move(rootdir_data+filename, rootdir_dst)