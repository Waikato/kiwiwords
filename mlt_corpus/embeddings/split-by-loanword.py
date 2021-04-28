#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#For training word embeddings
#One file per loanword

import pandas as pa
import re 

def split_by_loanword(inputFile):   
    tweets = pa.read_csv(inputFile, sep="\t")
    #tweets = tweets[(tweets['prob_relevant'] > 0.5)]
    #tweets = tweets.round({'prob_relevant':3})
    loanwords = tweets['loanword'].unique().tolist()
    for l in loanwords:
        tweets_for_l = tweets[tweets['loanword'] == l] 
        p = re.compile(r"^'|'$")
        filename = str(l).replace(" ","_")
        filename = p.sub(r"", filename) + ".csv"
        tweets_for_l.to_csv(filename, sep="\t", index = False)
    
split_by_loanword("mlt-corpus-rel.csv")
print("Done!")