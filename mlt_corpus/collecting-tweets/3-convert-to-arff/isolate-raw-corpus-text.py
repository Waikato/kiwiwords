#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 14:08:25 2019

@author: dgt12
"""

import re

def isolate_text(inputFile):
    goodTweets = []
    goodTweets.append("text\n")
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:
            p = re.compile(r'\d*","\S* \d*:\d*","\S*\s*\S*,"')
            line = p.sub(r"", line)
            p = re.compile(r'^"')
            line = p.sub(r"", line)
            p = re.compile(r'",\?$')
            line = p.sub(r"", line)            
            goodTweets.append(line)
    f.close()
    #Write to file
    outputFile = "text.csv"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    f.close()
    
def isolate_usernames(inputFile):
    goodTweets = []
    goodTweets.append("username\n")
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:
            p = re.compile(r'^"\d+"."(\S*[^,])"')
            line = p.sub(r"\1", line)
            p = re.compile(r',.*')
            line = p.sub(r"", line)
            goodTweets.append(line)
    f.close()
    #Write to file
    outputFile = "usernames.csv"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
    f.close() 

#isolate_text("loanwords.target.arff")
isolate_usernames("loanwords.target.arff")
print("Done!")