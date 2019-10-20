#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pa
import re

##########################################################################
#Tidies up Weka output, removes irrelevant tweets

#Tidy up Weka output
def format_corpus(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Reorder columns
    tweets = tweets[['id','username','timestamp','loanword','text','predicted','prediction']]
    #Change probabilites from p(majority_class) to p(relevant)
    tweets.loc[tweets['predicted'] == "2:non-relevant", 'prediction'] = 1-tweets['prediction']
    #Round to 3 d.p.
    tweets = tweets.round({'prediction':3})

    #Remove speechmarks around date and text
    tweets['timestamp'] = tweets['timestamp'].apply(lambda x: re.sub("^'|'$","", x))
    tweets['text'] = tweets['text'].apply(lambda x: re.sub("^'|'$","", x))
    #Remove backslash before apostrophes
    tweets['text'] = tweets['text'].apply(lambda x: re.sub(r"\\'","'", x))    
    tweets.to_csv("mlt-corpus-all.csv", sep="\t", index = False)
    
#Discard irrelevant tweets
def save_rel(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets[(tweets['predicted'] == "1:relevant")]
    #Remove "predicted" column (as all relevant)
    tweets = tweets[['id','username','timestamp','loanword','text','prediction']]
    tweets.to_csv("mlt-corpus-rel.csv", sep="\t", index = False) 
    
    
##########################################################################
#Removes duplicate tweets

#NB: Need to manually merge output
#Remove header from duplicates_fixed.csv
#Concatenate duplicates_fixed.csv with processed-rel-new, THEN remove speech marks and sort
#cat processed-rel-new.csv duplicates_fixed.csv > duplicates-removed.csv

#Extract duplicate tweets from processed corpus
def find_duplicate_ids(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    duplicate_tweets = tweets[tweets.duplicated(subset='id', keep=False)]
    #duplicate_tweets = tweets[tweets.duplicated(subset='id', keep="first")]
    duplicate_tweets.to_csv("duplicates2.csv", sep="\t", index=False) 

#Merge duplicate tweets, insert comma-separated loanwords
#Input = output of find_duplicate_ids
def combine_duplicates(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Get distinct ids
    ids = tweets['id'].unique()    
    #For each id
    for id in ids:
        #Extract all loanwords associated with that id
        loanwords = tweets.loc[tweets['id'] == id, 'loanword'].tolist()
        #Convert list into a single, comma-separated string
        loanwords_list = ",".join([str(x) for x in loanwords])
        #print(loanwords_list)
        #Update all 
        tweets.loc[tweets['id'] == id, 'loanword'] = loanwords_list
    tweets = tweets.drop_duplicates(subset='id', keep="first")
    tweets.to_csv("duplicates_fixed.csv", sep="\t", index=False)

#Remove duplicate tweets from processed corpus
def remove_duplicates(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    unique_tweets = tweets.drop_duplicates(subset='id', keep=False)
    unique_tweets.to_csv("processed-rel-new.csv", sep="\t", index=False)
    
#Removes speechmarks around query words that are phrases
#e.g. 'kia ora' -> kia ora
def remove_speech_marks(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets['loanword'] = tweets['loanword'].apply(lambda x: re.sub("'","", x))
    tweets.to_csv("duplicates-removed2.csv", sep="\t", index=False)

#Sort by loanword attribute
def sort(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets.sort_values(by ='loanword')
    tweets.to_csv("duplicates-removed-new.csv", sep="\t", index=False)
    
    
##########################################################################
#Extract ids for download script

def isolate_ids(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    ids = tweets['id'].astype(str)
    with open("ids-only.csv", 'w') as f:
        for tweet_id in ids:
            f.write(tweet_id + "\n")

##########################################################################
    
#format_corpus("naiveBayes-Bigrams-Pred-Target.csv")
#print("MLT Corpus formatted!")
#save_rel("mlt-corpus-all.csv")
#print("Irrelevant tweets removed!")
    
##########################################################################

##Remove duplicate tweets
#find_duplicate_ids("mlt-corpus-rel.csv")
#print("Duplicates found!")
#combine_duplicates("duplicates2.csv")
#print("Duplicates merged!")
#remove_duplicates("mlt-corpus-rel.csv")
#print("Duplicates removed!")
##MERGE FILES!
#remove_speech_marks("duplicates-removed.csv")
#print("Speech marks removed!")
#sort("duplicates-removed2.csv")
            
##########################################################################

#For downloading the corpus
#isolate_ids("duplicates-removed-new.csv")
            