#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import shutil

#Get current directory
DIR = os.path.dirname(os.path.realpath(__file__))    

#Merges two files (one with macrons, one without)
#e.g. "whāngai-macron.csv and whangai.csv" -> "whangai-merged.csv"
def merge_files():
    for root, dirs, files in os.walk(DIR, topdown=False):   
        for filename in files:
            if filename.endswith("-macron.csv"):
                inputFile1 = filename
                inputFile2 = filename.replace("-macron","")
                #Demacronise
                inputFile2 = inputFile2.replace("ā","a").replace("ē","e").replace("ī","i").replace("ō","o").replace("ū","u")
                #Output file
                outputFile = inputFile2.replace(".csv","") + "-merged.csv"    
                #https://codescracker.com/python/program/python-program-merge-two-files.htm 
                with open(outputFile, "wb") as wfd:
                    for f in [inputFile1, inputFile2]:
                        with open(f, "rb") as fd:
                            shutil.copyfileobj(fd, wfd, 1024*1024*10)
                print(inputFile1 + " and " + inputFile2 + " merged successfully!")
                
def removeTmpFiles():
    #Remove all CSV files except "-merged.csv" (cleaned data)
    pattern = "^((?!-merged\.csv|.py).)*$"
    for root, dirs, files in os.walk(DIR, topdown=False):
        for file in filter(lambda x: re.match(pattern, x), files):
            os.remove(os.path.join(root, file))

merge_files()
removeTmpFiles()