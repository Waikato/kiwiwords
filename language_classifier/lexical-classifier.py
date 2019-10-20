#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pa
from string import ascii_letters
import re

#Could automate entire process such that it reads and processes raw ARFF file output    

##########################################################################

#Get tweet text - filter out punctuation, emojis and numbers
def isolate_text(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets['text'].str.lower() 
    #Remove @user mentions (usernames won't help us discover loanwords)
    tweets = tweets.apply(lambda x: re.sub("@\S+","", str(x)))
    #Remove numbers (numbers won't help us discover loanwords)
    tweets = tweets.apply(lambda x: re.sub("\d+","", str(x)))
    with open("stripped.csv", 'w') as f:
        for tweet in tweets:
            #Remove punctuation and emojis
            tweet = tweet.replace(".","")
            permitted_chars = ascii_letters + " āēīōū"
            tweet = "".join(c for c in tweet if c in permitted_chars) 
            f.write(tweet + "\n")

##########################################################################
            
#Add unique words in corpus to text file
#https://stackoverflow.com/questions/37857080/add-unique-words-from-a-text-file-to-a-list-in-python
def get_words(f):
    illegal_chars = re.compile('[bcdfjlqsvxyz]')
    for line in f:
        for word in line.split():
            #print(word)
            if(illegal_chars.search(word) == None): 
                yield word

#with open('stripped.csv') as infile:
#    unique_words = sorted(set(get_words(infile)))
#
#with open('corpus_words.target.arff', 'w') as f:
#    f.write("""@relation training-words
#
#@attribute word string
#@attribute language {english,maori}
#
#@data\n""")
#    for item in unique_words:
#        f.write("%s,?\n" % item)
        

##########################################################################

#Discard words that were classified as English            
def save_rel(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets[(tweets['predicted'] == "2:maori")]
    #Remove "predicted" column (as all relevant)
    tweets = tweets[['prediction','word']]
    tweets.to_csv("maori-words.csv", sep="\t", index = False) 
            
##########################################################################               
#Get frequencies for all words (that were classified as Maori)
#Adapted from: https://www.codementor.io/isaib.cicourel/word-frequency-in-python-e7cyzy6l9

def tokenize():
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None

def map_book(tokens):
    hash_map = {}
    if tokens is not None:
        for word in tokens:
            if word in hash_map:
                hash_map[word] = hash_map[word] + 1
            else:
                hash_map[word] = 1
        return hash_map
    else:
        return None

file = open('stripped.csv', 'r')
book = file.read()
#Tokenize book
words = tokenize()
#Put all words that were classified as Maori in a list
lexicon = pa.read_csv("maori-words.csv", sep="\t")
word_list = lexicon['word'].tolist()
#Create hashmap
map = map_book(words)
#Save to file
with open('all_maori_word_frequencies.csv', 'w') as f:
    for word in word_list:
        f.write(word + "\t" + str(map[word]) + "\n")

print("Done!")

##########################################################################               

#isolate_text("duplicates-removed-new.csv")    
#print("Text isolated!")

#save_rel("liblinear-Pred-Target.csv")