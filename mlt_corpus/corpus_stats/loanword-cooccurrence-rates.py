#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pa
import numpy as np
import re

#Creates a loanword co-occurrence network
def create_matrix(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t")
    tweets = tweets['text']
    tweets = tweets.str.lower()
    #Remove macrons and hyphens
    macrons = {'ā':'a','ē':'e','ī':'i','ō':'o','ū':'u','-':''}
    for mac, plain in macrons.items():
        tweets = tweets.apply(lambda x: re.sub(mac,plain, str(x)))
    #Make dynamic by automatically detecting phrases in query word text file
    phrases = ['non maori','haere mai','kia ora','kapa haka','tena koutou','kia kaha','te reo','kai moana','tena koe','tangata whenua','wahi tapu']
    for p in phrases:
        tweets = tweets.apply(lambda x: re.sub(p,p.replace(" ", ""), str(x)))   
    #print(tweets)
    #words = ['aotearoa', 'talks', 'tea', 'bear']
    loanwords = pa.read_csv("query_words.csv")
    words = list(loanwords['query_words'])
    vectorizer = CountVectorizer(vocabulary=words)
    X = vectorizer.fit_transform(tweets)
    #print(X.toarray())
    np.savetxt("array.txt",X.toarray(),fmt="%s")
    
#Change this so that it's automatically appended as first line in array.txt
#aotearoa kiwi kiwis maori nonmaori pakeha haurangi porangi haeremai kiaora haka kapahaka tenakoutou whakapapa kiakaha kowhai whanau matariki hangi iwi marae pounamu tereo wahine tamariki kaimoana whare tenakoe whenua korero powhiri taniwha hongi morena tangatawhenua kakariki puku karakia kohanga kahurangi hapu tangata waiata taonga rangatiratanga tangi kaumatua kaupapa rangatira tikanga whero mokopuna kainga maunga whakarongo wahitapu wananga kaitiaki hikoi papatuanuku katoa atua tupuna whangai kuia korowai taiaha mawhero tohunga waewae whaea teina hoha tuakana manuhiri kawanatanga taihoa total
def get_header(inputFile):
    loanwords = pa.read_csv("query_words.csv")
    words = list(loanwords['query_words'])
    converted = (str(w) for w in words)
    converted = ' '.join(converted) 
    print(converted + " total")
    
def tally_occurrences(inputFile):
    totals = []
    with open(inputFile, 'r') as f:
        for line in f:
            line2 = [int(i) for i in line.split()]
            tally = sum(line2)
            print(tally)
            line = line.rstrip()
            if(tally > 2):
                line += " " + str(tally) + "\n"
                totals.append(str(line))        
    outputFile = "array.txt"    
    with open(outputFile, 'w') as f:
        for t in totals:
            f.write(t)

#APPEND HEADER 
#Read all terms from "query_words.csv", replace \n with "s"
def reduce_sparsity(inputFile):
    multiple_loanwords = []
    with open(inputFile, 'r') as f:
        for line in f:
            if line.count("1") > 1:
                multiple_loanwords.append(line)
    #Write to file
    outputFile = "array-new.txt"    
    with open(outputFile, 'w') as f:
        for t in multiple_loanwords:
            f.write(t)

#Loanword co-occurrence networks    
#create_matrix("duplicates-removed-new.csv")
#reduce_sparsity("array.txt")
#tally_occurrences("array-new.txt")
