#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pa
import re
import string
import os

##########################################################################

#Extract ALL HASHTAGS (not just hybrids) and report how many times they occur each year.   
#Manually label hashtags as hybrid or non-hybrid.
def get_hashtag_frequencies(inputFile):
    table_rows = []
    table_rows.append("hashtag\tnum_tweets\tnum_appearances\t2007\t2008\t2009\t2010\t2011\t2012\t2013\t2014\t2015\t2016\t2017\t2018\tdistinct_users\n")
    tweets = pa.read_csv(inputFile, sep="\t")
    text = tweets['text']
    hashtags = dict(text.str.extractall(r"(\#\w+)")[0].value_counts())
    for h, v in hashtags.items():
        if v > 9:
            print(h)
            #print(v)
            #Don't count sub-hashtags (e.g. #kiwis doesn't count #kiwi)
            tweets_containing_hashtag = tweets[tweets['text'].str.contains(h + r'[ ,.#!)@?]')|tweets['text'].str.endswith(h)]
            users = len(tweets_containing_hashtag['username'].unique())
            counts = get_year_counts(tweets_containing_hashtag)
            total = sum(counts.values())
            #print(total)
            final = pa.DataFrame([counts.values()]).to_string(header=False, index=False).replace("  ", "\t")
            table_rows.append(h + "\t" + str(total) + "\t" + str(v) + "\t" + final + "\t" + str(users) + "\n")    
    #Write to file
    outputFile = "diachronic-hashtags-new.csv"    
    with open(outputFile, 'w') as f:
        for t in table_rows:
            f.write(t)

##########################################################################
    
#Requires list of hybrid hashtags
def extract_hybrid_tweets(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Convert all tweet text to lowercase
    tweets['text'] = tweets['text'].str.lower() 
    #Read in hybrid hashtags
    hashtags = pa.read_csv("hybrids.csv") 
    #Convert to list
    hybrids = list(hashtags['hashtag'])
    #hybrids = hybrids.sort()
    #Index for filename
    count = 1
    #For each hybrid hashtag
    for hybrid in hybrids:
        print(hybrid)
        #Consolidate all variants of the hashtag
        #1) Lowercase, #2) Demacronise, #3) Search for pluralised form (-s), #4) Hardcoded hashtags
        #Convert all characters in hashtag to lowercase
        hybrid = hybrid.lower()
        #Convert macron (ā) into non-macron (a) 
        if "ā" in hybrid:
            #e.g. replace #beingmāori with #beingmaori
            tweets['text'] = tweets['text'].apply(lambda x: re.sub(hybrid,hybrid.replace("ā", "a"), str(x)))
        hybrid = hybrid.replace("ā","a")
        if hybrid == "#proudtobeakiwi" or hybrid == "#youknowyoureakiwiwhen":
            tweets['text'] = tweets['text'].apply(lambda x: re.sub(hybrid,hybrid.replace("a", ""), str(x)))
            hybrid = hybrid.replace("a","")
        if hybrid in ["#flyingkiwis", "#gokiwis", "#ilovekiwis", "#kiwitweets", "#lovekiwis", "#proudkiwis"]:
            tweets['text'] = tweets['text'].apply(lambda x: re.sub(hybrid,hybrid.replace("s", ""), str(x)))
            hybrid = hybrid.replace("s","")
        #Find all tweets containing that hashtag
        hybrid_tweets = tweets[tweets['text'].str.contains(hybrid + r'[ ,.#!)@?]')|tweets['text'].str.endswith(hybrid)]
        #Save to CSV
        hybrid_tweets.insert(loc=0,column='hybrid_hashtag',value=hybrid)
        #Get the current directory
        DIR = os.path.dirname(os.path.realpath(__file__))
        path=DIR + r'/hybrids/'
        #Rename 1-9 to 01-09
        if(count<10):
            hybrid_tweets.to_csv(path + "0" + str(count) + "_" + hybrid + ".csv", sep="\t", index=False, header=False) 
        else:
            hybrid_tweets.to_csv(path + str(count) + "_" + hybrid + ".csv", sep="\t", index=False, header=False) 
        print(hybrid)
        count+=1
    #Then concatenate all files in directory: all-hybrid-tweets.csv
    #Add header!
    #hashtag\tid\tusername\ttimestamp\tloanword\ttext\tprediction
    #Input for hybrids_to_individual_text_files?

#Calculates individual word counts for each tweet
def get_tweet_word_counts(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets['text']
    word_count = []
    with open(inputFile, 'w') as f:
        for tweet in tweets:
            tweet = tweet.replace(".","")
            tweet = tweet.translate(str.maketrans('','',string.punctuation))
            tweet = tweet.translate(str.maketrans('','','ヾ≧∇≦ゝﾉ･・∀☆∗•̀＊□〇́▽■˚☐˘ง'))
            num_words = len(tweet.split())
            word_count.append(str(num_words))
            #Could add number of words in hashtag (by looking it up in a dictionary file)
            f.write(tweet + "\t" + str(num_words) + "\n")    
                        
##########################################################################
            
#Converts hybrid tweets into a suitable format for processing in Antconc
#One file per tweet

#Input file:
#hybrid_hashtag\tinst#\actual\predicted\error\prediction\id\username\timestamp\loanword\text
#nethui	9511	1:?	1:relevant		0.997	928741619691487230	StuFlemingNZ	2017-11-10 10:50	aotearoa	This is a true story about New Zealand and the Internet.' 'A unique piece of Internet history from an Aotearoa perspective ' #nethui #nethuinz @hollowaysmith

def hybrids_to_individual_text_files(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    hybrid_hashtags = tweets['hashtag'].unique().tolist()
    
    for h in hybrid_hashtags:
        print(h)
        hybrid_hashtag = (str(h)).replace("'","")
        hybrid_hashtag = hybrid_hashtag.replace(" ","_")

        tweets = pa.read_csv(inputFile, sep="\t")
        #tweets['loanword'] = tweets['loanword'].apply(lambda x: re.sub(r" ","_", x))
        tweets = tweets[(tweets['hashtag'] == hybrid_hashtag)]
        #Get username and date
        text = dict(tweets['text'])
        usernames = dict(tweets['username'])
        dates = dict(tweets['timestamp'])    
        
        for username in usernames:
            current_text = str(text[username])
            current_date = str(dates[username])
            p2 = re.compile(r' \d\d:\d\d')
            current_date = p2.sub(r'', current_date)
            filename = str(username+1) + "_" + str(usernames[username]) + "_" + current_date + ".txt"
            writeToCSV(current_text, filename, h)
        
def writeToCSV(current_text, filename, hashtag):
    #https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
    DIR = "/home/dgt12/Documents/antconc"
    if not os.path.exists(DIR + "/" + hashtag):
        os.makedirs(DIR + "/" + hashtag)
    outputFile = DIR + "/" + hashtag + "/" + filename
    #print("Processing %s..." % filename)
    with open(outputFile, 'w') as f:
        f.write(current_text)

##########################################################################

#Calculate diachronic frequences for HYBRID hashtags only    
def get_hybrid_frequencies(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    table_rows = []
    table_rows.append("hashtag\tnum_tweets\t2007\t2008\t2009\t2010\t2011\t2012\t2013\t2014\t2015\t2016\t2017\t2018\tdistinct_users\n")
    hashtags = pa.read_csv("hybrids.csv")
    hybrids = list(hashtags['hashtag'])   
    #hybrids = hybrids.sort()
    for hybrid in hybrids:
        hybrid = hybrid.lower()
        hybrid = hybrid.replace("ā","a")
        if hybrid == "#proudtobeakiwi" or hybrid == "#youknowyoureakiwiwhen":
            hybrid = hybrid.replace("a","")
        if hybrid in ["#flyingkiwis", "#gokiwis", "#ilovekiwis", "#kiwitweets", "#lovekiwis", "#proudkiwis"]:
            hybrid = hybrid.replace("s","")
        tweets_containing_hashtag = tweets[tweets['text'].str.contains(hybrid + r'[ ,.#!)@?]')|tweets['text'].str.endswith(hybrid)]
        print(hybrid)
        users = len(tweets_containing_hashtag['username'].unique())
        counts = get_year_counts(tweets_containing_hashtag)
        total = sum(counts.values())
        final = pa.DataFrame([counts.values()]).to_string(header=False, index=False).replace("  ", "\t")
        table_rows.append(hybrid + "\t" + str(total) + "\t" + "\t" + final + "\t" + str(users) + "\n")    
        #Write to file
    outputFile = "diachronic-hybrid-frequencies.csv"    
    with open(outputFile, 'w') as f:
        for t in table_rows:
            f.write(t)
            
def get_year_counts(tweets):
    y_keys = ["2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]
    y_values = []
    index = 0
    for year in y_keys:
        count = len(tweets[tweets['timestamp'].str.contains(year)])
        y_values.insert(index, count)
        index+=1
    year_counts = dict(zip(y_keys, y_values))
    return year_counts  

##########################################################################
        
#get_hashtag_frequencies("duplicates-removed-new.csv")

#extract_hybrid_tweets("test3.csv")
#extract_hybrid_tweets("duplicates-removed-new.csv")
#Get individual word counts for each tweet
#get_tweet_word_counts("all-hybrid-tweets.csv")

#hybrids_to_individual_text_files("all-hybrid-tweets.csv")    

#get_hybrid_frequencies("all-hybrid-tweets.csv")                   

#print("Done!")