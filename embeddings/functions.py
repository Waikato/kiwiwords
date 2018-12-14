#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 15:08:36 2018

@author: fbravoma
"""

import glob
import pandas as pa
from .twokenize import tokenizeRawTweetText


def corpus2plainfile(source,target,extension='csv',col_name='text',sep="\t"):
        """
        converts a folder with csv files into a single file including just the tweet content. 
        Tweet are tokenized with tweetNLP and lowercased.
        One line per tweet.
        """    
       
        
        with open(target, 'a') as out_file:
            #os.chdir(source)
            csv_files = [i for i in glob.glob(source+'/*.{}'.format(extension))]
            print(csv_files)
            for file in csv_files:
                tweets = pa.read_csv(file,sep=sep)
                for tweet in tweets[col_name]:
                    clean_tweet = ' '.join(tokenizeRawTweetText(tweet.lower()))
                    out_file.write(clean_tweet+"\n")



