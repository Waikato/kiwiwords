#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pa
import re
import string

##########################################################################

#Corpus Overview
def isolate_text(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets['text'].astype(str)
    with open("text-only.csv", 'w') as f:
        for tweet in tweets:
            tweet = tweet.replace(".","")
            tweet = tweet.translate(str.maketrans('','',string.punctuation))
            #This doesn't capture everything
            #Should really change it so it only accepts ASCII chars and numbers
            tweet = tweet.translate(str.maketrans('','','ヾ≧∇≦ゝﾉ･・∀☆∗•̀＊□〇́▽■˚☐˘ง'))
            f.write(tweet + "\n")
            
def get_num_words(inputFile):
    with open(inputFile, encoding="utf8") as f:
        num_lines = 0
        num_words = 0
        for line in f:
            num_lines += 1
            num_words += len(line.split())
        print("Number of tweets: " + str(num_lines))
        print("Number of words: " + str(num_words))
        
def get_num_tweeters(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    num_users = len(tweets['username'].unique().tolist())
    print("Number of users: " + str(num_users))

##########################################################################
    
#Calculates the number of OCCURRENCES of each (query) loanword per year
#EDIT: Add the ability to calculate the number of DISTINCT USERS of each (query) loanword per year
def get_diachronic_stats(inputFile): 
    results = []
    pa.set_option('display.max_rows', 1000)
    tweets = pa.read_csv(inputFile, sep="\t")
    #Read in list of query words
    query_words = pa.read_csv("query_words.csv")
    loanwords = list(query_words["query_words"])
    years = ["2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018"]

    #For each year
    for year in years:
        print(year)
        results.append(year)
        #Get all tweets for the current year
        curr_year = tweets[tweets['timestamp'].str.contains(year)]
        #Convert text to lowercase
        text = curr_year['text'].str.lower()
        #remove hyphens
        text = text.apply(lambda x: re.sub("-","", str(x)))
        #remove macrons
        macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
        for mac, plain in macrons.items():
            text = text.apply(lambda x: re.sub(mac,plain, str(x)))
        #remove spaces from phrases
        phrases = ['non maori','haere mai','kia ora','kapa haka','tena koutou','kia kaha','te reo','kai moana','tena koe','tangata whenua','wahi tapu']
        for p in phrases:
            text = text.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))
        #Count number of occurrences of each loanword in current year
        counts = pa.Series((text.astype(str).str.count(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords), loanwords, name='count')
        results.append(counts)
    
    #Write to file
    outputFile = "query_word_diachronic_frequencies.csv"    
    with open(outputFile, 'w') as f:
        for r in str(results):
            f.write(r)    

##########################################################################
    
#Get number of TWEETS containing each query word in the corpus
#Doesn't capture mispellings or plurals with different spelling (e.g. taiahas)
def get_tweet_frequencies(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Convert tweet text to lowercase
    text = tweets['text'].str.lower()
    #Remove hyphens
    text = text.apply(lambda x: re.sub("-","", str(x)))
    #Remove macrons (to include macron query words in count)
    macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
    for mac, plain in macrons.items():
        text = text.apply(lambda x: re.sub(mac,plain, str(x)))
    #Make dynamic by automatically detecting phrases in query word text file
    phrases = ['non maori','haere mai','kia ora','kapa haka','tena koutou','kia kaha','te reo','kai moana','tena koe','tangata whenua','wahi tapu']
    for p in phrases:
        text = text.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))
    #print(text)
    #Read in query words
    query_words = pa.read_csv("query_words.csv")
    loanwords = list(query_words["query_words"])
    #Doesn't include loanwords that are substrings (e.g. 'iwi' in 'kiwi')
    #Words that don't have loanwords as a substring ('kiwi' in 'kiwifruit')
    #regex = beginning_ | _middle_ | _end
    #Doesn't pick up "kiwi kiwi" twice..
    #COMMENTED ONE IS NEATER!
    #counts = pa.Series((text.str.contains(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords), loanwords, name='count')
    counts = {lw: text.str.contains(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords}
    print(counts)
    #phrases: shorter doesn't count longer because of the early space removal
    #superphrases = ["nonmaori", "tangatawhenua","tangatawhenua","kapahaka"]
    #subphrases = ["maori", "tangata", "whenua", "haka"]
    
    #Export frequencies to CSV
    #https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi    
    counts = pa.DataFrame(counts, index=[0])
    counts.T.reset_index().to_csv('query_word_freqs.csv', header=False, index=False)

#COUNTS NUM OCCURRENCES OF EACH LOANWORD
def get_lw_occurrences(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Convert tweet text to lowercase
    text = tweets['text'].str.lower()
    #Remove hyphens
    text = text.apply(lambda x: re.sub("-","", str(x)))
    #Remove macrons (to include macron query words in count)
    macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
    for mac, plain in macrons.items():
        text = text.apply(lambda x: re.sub(mac,plain, str(x)))
    #Make dynamic by automatically detecting phrases in query word text file
    phrases = ['non maori','haere mai','kia ora','kapa haka','tena koutou','kia kaha','te reo','kai moana','tena koe','tangata whenua','wahi tapu']
    for p in phrases:
        text = text.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))
    #print(text)
    #Read in query words
    query_words = pa.read_csv("query_words.csv")
    loanwords = list(query_words["query_words"])
    #Doesn't include loanwords that are substrings (e.g. 'iwi' in 'kiwi')
    #Words that don't have loanwords as a substring ('kiwi' in 'kiwifruit')
    #regex = beginning_ | _middle_ | _end
    #Doesn't pick up "kiwi kiwi" twice..
    counts = pa.Series((text.str.count(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords), loanwords, name='count')
    print(counts)
    #phrases: shorter doesn't count longer because of the early space removal
    #superphrases = ["nonmaori", "tangatawhenua","tangatawhenua","kapahaka"]
    #subphrases = ["maori", "tangata", "whenua", "haka"]
    #Export frequencies to CSV
    #https://stackoverflow.com/questions/17839973/constructing-pandas-dataframe-from-values-in-variables-gives-valueerror-if-usi    
    counts.to_csv('query_word_occurrences.csv', header=False, index=True)

##########################################################################

#Could combine with no_macron (same method), by changing all macrons to non-macrons after initial processing 
def get_macron_frequencies(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Convert tweet text to lowercase
    text = tweets['text'].str.lower()
    #Remove hyphens
    text = text.apply(lambda x: re.sub("-","", str(x)))
    #Make dynamic by automatically detecting phrases in query word text file
    mac_phrases = ['non māori','tēnā koutou','tēnā koe','wāhi tapu']
    for p in mac_phrases:
        text = text.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))
    #print(text)
    #Read in query words
    query_words = pa.read_csv("macron_query_words.csv")
    loanwords = list(query_words["query_words"])
    counts = pa.Series((text.str.count(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords), loanwords, name='count')
    print(counts)
    counts.to_csv('macron_query_word_occurrences.csv', header=False, index=True)

def get_macron_removed_frequencies(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    #Convert tweet text to lowercase
    text = tweets['text'].str.lower()
    #Remove hyphens
    text = text.apply(lambda x: re.sub("-","", str(x)))
    #Make dynamic by automatically detecting phrases in query word text file
    non_mac_phrases = ['non maori','tena koutou','tena koe','wahi tapu']
    for p in non_mac_phrases:
        text = text.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))
    #print(text)
    #Read in query words
    query_words = pa.read_csv("macron_removed_query_words.csv")
    loanwords = list(query_words["query_words"])
    counts = pa.Series((text.str.count(r'^' + lw +'[\W_]|[\W_]' + lw + '[\W_]|[\W_]' + lw + '$').sum() for lw in loanwords), loanwords, name='count')
    print(counts)
    counts.to_csv('macron_removed_query_word_occurrences.csv', header=False, index=True)

##########################################################################

#Corpus Overview
#get_num_words(isolate_text("duplicates-removed-new.csv"))
#get_num_tweeters("duplicates-removed-new.csv")

##########################################################################

#Diachronic stats
#get_diachronic_stats("duplicates-removed-new.csv")
#print("Done!")

##########################################################################
    
#Loanword stats
#get_tweet_frequencies("duplicates-removed-new.csv")
#print("Computed tweet frequencies!")
#get_lw_occurrences("duplicates-removed-new.csv")
#print("Computed loanword occurrences!")

##########################################################################

#Macron stats
#get_macron_frequencies("duplicates-removed-new.csv")
#print("Computed macron frequencies!")
#get_macron_removed_frequencies("duplicates-removed-new.csv")
#print("Computed macron-removed frequencies!")