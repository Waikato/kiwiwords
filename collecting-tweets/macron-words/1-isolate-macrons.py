#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

#Get current directory
DIR = os.path.dirname(os.path.realpath(__file__))    
    
#Removes all tweets WITHOUT macrons from the given CSV file
def isolate_macrons():
    #pattern = "[ā|ē|ī|ō|ū]+.*\.csv$"
    for root, dirs, files in os.walk(DIR, topdown=False):   
        for filename in files:
            macronTweets = []
            if filename.endswith(".csv"):
                word = filename.replace(DIR + "/", "").replace(".csv", "")
                #Join filename with path to get location
                filePath = os.path.join(root, filename)    
                print("Processing %s..." % filename)
                #Read file
                with open(filePath, 'r') as fileinput:
                    for line in fileinput:
                        line2 = line.lower()
                        #Exclude tweets with links, "porn" and retweets
                        if word in line2 and "http:" not in line2 and "porn" not in line2 and line2.count("https") == 1 and '"rt' not in line2:
                            macronTweets.append(line)
                #Write to file
                with open(filePath.replace(".csv","") + "-macron.csv", 'w') as fileinput:
                    for tweet in macronTweets:
                        fileinput.write(tweet)

def removeTmpFiles():
    #Remove all CSV files except "-good.csv" (cleaned data)
    pattern = "^((?!-macron\.csv|.py).)*$"
    for root, dirs, files in os.walk(DIR, topdown=False):
        for file in filter(lambda x: re.match(pattern, x), files):
            os.remove(os.path.join(root, file))
                
isolate_macrons()
removeTmpFiles()
print("Done!")