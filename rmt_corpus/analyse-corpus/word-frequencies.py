#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import pandas as pa
import numpy as np

"""This script calculates Māori word frequencies in the RMT Corpus. 
Only individual words are considered (not multi-word phrases)!"""

#Get current directory
DIR = os.path.dirname(os.path.realpath(__file__))

#Extract tweet text from dataframe
def isolate_text(input_file, output_file):
    tweets = pa.read_csv(input_file, sep="\t")
    tweets = tweets['content'].astype(str)
    tweets.to_csv(output_file, sep="\t", header = True, index = False)
           
#Saves prep-processed text to file.
#There are different options available (see flags below).    
#Doesn't attempt to macronise words where macron has been omitted;
#would need to run a macroniser (e.g. http://community.nzdl.org/macron-restoration/jsp/en/main.jsp) to do that
#NB: Spaces are important for word counts (e.g. when removing punctuation)
def preprocess_twitter_data(input_file, output_file, output_file2, 
                            remove_numbers, remove_macrons, 
                            remove_hyphens, remove_hashtags, 
                            collapse_repeated_vowels, collapse_double_vowels):
    #remove_numbers: If True, removes the numbers [1234567890]
    #remove_macrons: If True, merges macrons and non-macrons ("māori" -> "maori")
    #remove_hyphens: If True, replaces hyphens with space (e.g. "hi-there" -> "hi there")
    #remove_hashtags: 
    #1) "keep" (as hashtag, e.g. #tereo)
    #2  "remove_symbol" with hashtag removed (e.g. tereo)
    #3) "exclude" (e.g. 'hi #tereo' -> 'hi')
    #collapse_repeated_vowels: If True, aaaaa -> a
    #collapse_double_vowels: If True, aa -> ā
    tweets = pa.read_csv(input_file, sep="\t")
    #Isolate tweet text
    tweets = tweets['content'].astype(str)
    all_double_vowel_words = []
    with open(output_file, 'w', encoding="utf8") as f:
        for tweet in tweets:
            #Convert text to lowercase
            tweet = tweet.lower()
            #Remove all instances of <link> and <user>
            tweet = tweet.replace("<link>","")
            tweet = tweet.replace("<user>","")                         
            #Replace selected punctuation with a single space
            #This ensures two words separated by a slash, for instance, 
            #are not merged together (e.g. forward/slash -> forward slash)
            tweet = re.sub(r"[,.;@?!&$/]+\ *", " ", tweet)
            #Remove remaining punctuation (exc. hashtags, hyphens) and numbers
            permitted_chars = "abcdefghijklmnopqrstuvwxyzāēīōū-#_ "
            
            if not remove_numbers:
                permitted_chars += "1234567890"
            
            tweet = "".join(c for c in tweet if c in permitted_chars)
            #Remove hyphens that are not part of words
            tweet = re.sub(r"^-| - |-$", " ", tweet)
            #If user wants to remove hyphens
            #i.e. treat hyphenated words as separate words
            if remove_hyphens:
                tweet = tweet.replace("-", " ")

            #If user wants to remove repeated vowels
            #e.g. 'raaaawe' -> 'rawe, "rangimaaaaarie" -> "rangimarie 
            #Note that this isn't ideal because the middle 'a' should have a 
            #macron - but then again author hasn't used one anyway)
            #Shouldn't really allow hashtags to be modified, if there are any 
            #that match...
            #Also shouldn't remove numbers from hashtags!!!
            if collapse_repeated_vowels:            
                vowels = ['a','ā','e','ē','i','ī','o','ō','u','ū']
                for vowel in vowels:
                    tweet = re.sub(r"" + vowel + "{3,}", vowel, tweet)
            
            #If user wants to collapse double vowels
            if collapse_double_vowels:
                double_vowels = ['aa','ee','ii','oo','uu']
                #Generate a list of words containing double vowels
                for word in tweet.split():
                    for double_vowel in double_vowels:
                        if double_vowel in word:
                            #print(word)
                            all_double_vowel_words.append(word)                    
           
            #If user wants to remove macrons
            #i.e. merge macron and non-macron variants of word
            if remove_macrons:
                macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u'}
                for mac, plain in macrons.items():
                    tweet = tweet.replace(mac, plain)
            
            #If user wants to remove hashtags
            if(remove_hashtags == "exclude"):
                hashtags = re.compile(r"(#\w+)")
                tweet = hashtags.sub(r"", tweet)
            #If user wants to remove '#' symbol but keep the text
            elif(remove_hashtags == "remove_symbol"):
                hashtags = re.compile(r"#(\w+)")
                tweet = hashtags.sub(r"\1", tweet)
        
            #Replace multiple spaces with single space
            tweet = re.sub(" {2,}", " ", tweet)
            #Remove leading spaces
            tweet = re.sub("^ {1,}", "", tweet)
            #Remove trailing spaces
            tweet = re.sub(" {1,}$", "", tweet)
            
            #Write to file           
            f.write(tweet + "\n")
        
        if collapse_double_vowels:
            all_doubles = sorted(set(all_double_vowel_words))
            with open(output_file2, 'w', encoding="utf8") as f:        
                print("word\n" + "\n".join(all_doubles), file=f)

#Before running, remove words that are obviously English from "output-doubles.csv"
#This code is not very elegant - could be refactored.
def substitute_double_vowels(input_file1, input_file2, input_file3, output_file):
    double_vowels = pa.read_csv(input_file1)
    double_vowels = double_vowels['word'].tolist()
    #print(double_vowels)
    stoplist = pa.read_csv(input_file2, sep="\t")
    stoplist = stoplist['word'].tolist()
    stoplist.extend(["tweet", "retweet"])
    #print(stoplist)
    #Remove worsd that are in the stoplist, then replace double vowels in 
    #all remaining words with macrons
    good_words = sorted(set(double_vowels) - set(stoplist))
    print("There are {} double vowel words that need replacing:".format(len(good_words)))
    print(good_words)
    double_vowels = {'aa':'ā','ee':'ē','ii':'ī','oo':'ō','uu':'ū'}
    with open(output_file, 'w', encoding='utf8') as writer:
        with open(input_file3, encoding="utf8") as f:
            for line in f:
                for word in good_words:
                    if word in line:
                        for doub, mac in double_vowels.items():
                            line = re.sub(word, word.replace(doub, mac), line)
                #Write to file           
                print(line, end="", file=writer)
                        
def get_num_words(input_file, hyphen_as_delimiter):
    with open(input_file, encoding="utf8") as f:
        num_lines = 0
        num_words = 0
        for line in f:
            if hyphen_as_delimiter:
                #Treat hyphen as word separator
                line = line.replace("-", " ")
            num_lines += 1
            num_words += len(line.split())
        print("Number of tweets: " + str(num_lines))
        print("Number of words: " + str(num_words))
    
#Get word frequencies
def tokenize(book):
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None
#Don't accept "nan" and "null" -> add these manually...
def map_book(tokens):
    hash_map = {}
    if tokens is not None:
        for word in tokens:
            if word in hash_map:
                hash_map[word] += 1
            else:
                hash_map[word] = 1
        return hash_map
    else:
        return None

def get_counts(text, word_types, output_file):
    file = open(text, 'r', encoding='utf-8')
    book = file.read()
    #Tokenize book
    words = tokenize(book)
    lexicon = pa.read_csv(word_types, sep="\t")
    word_list = lexicon['word'].tolist()
    #Create hashmap
    map = map_book(words)
    #Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("word\tfreq\n")
        for word in word_list:
            f.write(str(word) + "\t" + str(map[word]) + "\n")
    f.close()
    
def get_wordlist(input_file, output_file):
    with open(output_file, 'w', encoding="utf8") as writer:
        with open(input_file, 'r', encoding="utf8") as f:
            words = f.read().split()
            words = sorted(list(set(words)))
            writer.write("word\n")
            chars = set('abcdefghijklmnnopqrstuvwxyzāēīōū1234567890')
            for word in words:
                if word != "nan" and any((c in chars) for c in word):
                    writer.write(word + "\n")
        f.close()
    writer.close()

def reorder_freq(input_file, output_file):
    data = pa.read_csv(input_file, sep="\t")
    #data = data.sort_values(by ='freq', ascending=False)
    #Sort first by frequency, then alphabetically
    data = data.sort_values(['freq', 'word'], ascending=[False, True])
    data.to_csv(output_file, sep="\t", header = True, index = False)

#Write a function to isolate macron words and function words
def isolate_macron_words(input_file, output_file):
    words = pa.read_csv(input_file, sep="\t")
    words = words[words['word'].str.contains('ā|ē|ī|ō|ū')]
    words.to_csv(output_file, sep="\t", header = True, index = False)

#Requires a list of function words
def isolate_function_words(input_file, input_file2, output_file):
    words = pa.read_csv(input_file, sep="\t")
    function_words = pa.read_csv(input_file2, sep="\t")
    all_function_words =  function_words['word'].tolist()
    words = words[np.isin(words, all_function_words).any(axis=1)]
    words.to_csv(output_file, sep="\t", header = True, index = False)

def isolate_content_words(input_file, input_file2, output_file):
    words = pa.read_csv(input_file, sep="\t")
    function_words = pa.read_csv(input_file2, sep="\t")
    all_function_words =  function_words['word'].tolist()
    words = words[~np.isin(words, all_function_words).any(axis=1)]
    words.to_csv(output_file, sep="\t", header = True, index = False)

def calc_normalised_freq(input_file, output_file):
    words = pa.read_csv(input_file, sep="\t")
    #Absolute ranking (allows for ties)
    words['rank'] = words['freq'].rank(ascending=False, method="min").astype(int)
    total = words['freq'].sum()
    print("Total words:", total)
    #words['percentage'] = round(words['freq']/total*100,2)
    words['normalised_per_10000'] = round((words['freq']/total) * 10000,0).astype(int)
    #words['percentage'] = words['percentage'].apply(str) + "%"
    words = words[['rank', 'word', 'freq', 'normalised_per_10000']]
    words.to_csv(output_file, sep="\t", header = True, index = False)

#Run a separate hashtag analysis (don't want to modify hashtags!)
def get_rmt_corpus_frequencies():
    #isolate_text("rmt-corpus-v1.csv", "text-only.csv")
    preprocess_twitter_data("rmt-corpus-v1.csv", "rmt-preprocessed.csv", 
                            "output_doubles.csv", False, False, False, "keep",
                            False, False)
    #NEED TO MANUALLY CHECK "output_doubles.csv" BEFORE RUNNING THIS!!!
    #will need to remove anything containing "tweets"
    #substitute_double_vowels("output_doubles.csv","double_vowel_words_new.csv", 
    #                         "rmt-preprocessed.csv", "rmt-preprocessed2.csv")
    get_num_words("rmt-preprocessed.csv", False)    
    get_wordlist("rmt-preprocessed.csv", "wordlist.csv")
    get_counts("rmt-preprocessed.csv", "wordlist.csv", "freq-alph.csv")
    reorder_freq("freq-alph.csv", "frequencies.csv")
    calc_normalised_freq("frequencies.csv","rmt-percentages.csv")
    isolate_macron_words("rmt-percentages.csv", "rmt-freq-mac.csv")
    isolate_function_words("rmt-percentages.csv", "function_words_macronised.csv", 
                       "rmt-freq-func.csv")
    isolate_content_words("rmt-percentages.csv", "function_words_macronised.csv", 
                       "rmt-freq-content.csv")
    
get_rmt_corpus_frequencies()
print("Done!")