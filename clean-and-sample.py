#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Import Python libraries
import csv
import random
import os
import re
import pandas as pa

#INSERT DIRECTORY PATH HERE
#For program to work, folder must be empty apart from this Python file and CSVs to run it on. Move output to another (non-sub) folder. 
DIR = "/home/dgt12/Documents/code/corpus/new"
#Global flag - If file already in TSV format, set to True
TSV = False

#Cleans Tweets by removing retweets (marked with 'rt'), blank lines and Tweets where username contains loanword (e.g. @kiwi, @happy_kiwi).
#If TSV = False, converts "raw" data to TSV, replacing semi-colons (;) with '\t'.
def cleanTweets(inputFile):
    goodTweets = []
    #Insert header
    if not TSV:
        goodTweets.append("username\tdate\tretweets\tfavourites\ttext\tgeo\tmentions\thashtags\tid\tpermalink\n")
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:
            #Convert data to lowercase
            line2 = line.lower()
            #Extract loanword from filepath
            word = inputFile.replace(DIR + "/", "").replace(".csv", "")
            #Regular expression to find users whose username contains a loanword (e.g. @happy_kiwi) 
            username = re.compile('[@|_]\S*' + word.lower())
            #pattern = re.compile('[^_|@|]' + word.lower())
            
            if not TSV:
                #Constant to store number of coloumns of data; this number minus one is the number of semi-colons we expect to read in
                NUM_COLUMNS = 10;
                #If Tweet text contains at least one semi-colon 
                if line.count(";") > (NUM_COLUMNS - 1):
                    #Get number of semi-colons in Tweet
                    semicolonsInTweet = line2.count(";") - (NUM_COLUMNS - 1)
                    #For each semi-colon in Tweet
                    for i in range(semicolonsInTweet):
                        #Remove semi-colon from Tweet
                        line = replaceOccurrence(line, ";", ",", 4) 
                
                #Remove any tabs already in Tweet
                line = line.replace("\t", "")
                #Replace all (remaining) semi-colons with tab delimiter
                line = line.replace(";", "\t")
            
            #Remove retweets, blank lines and old-style headings
            if '"rt' not in line2 and "username;date;retweets" not in line2 and line2 != "\n": #and PHRASE not in line2
                #Remove tweets containing loanword in username
                if(username.search(line2) == None):
                #if(username.search(line2) == None or pattern.search(line2) != None):
                    #Add all other tweets to list
                    goodTweets.append(line)

    #Write to file
    outputFile = DIR + "/" + word + "-duplicates.csv"    
    with open(outputFile, 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
                        
#Replaces the nth occurrence of the given substring.
#Copied from https://forums.cgsociety.org/t/python-how-to-replace-nth-occurence-of-substring/1562801/2 
def replaceOccurrence(str, search, replacement, index):
    split = str.split(search, index + 1)
    if len(split) <= index + 1:
        return str
    return search.join(split[:-1]) + replacement + split[-1]

#Removes Tweets that have different id's but identical or almost identical text (i.e. same wording but slightly different punctuation and/or spelling). 
def removeSimilarTweets(inputFile):
    #Extract loanword from filename
    word = inputFile.replace(DIR + "/", "").replace("-duplicates.csv", "")
    #Make dataframe from CSV file
    tweets = pa.read_csv(inputFile, sep="\t")
    #Avoid rounding id's when merging
    tweets['id'] = tweets['id'].apply("int64")
    #Create copy of dataframe to preserve original formatting
    original = tweets.copy(deep=True)
    #Drop successive duplicate (or near-duplicate) tweets
    tweets['text'] = tweets['text'].str.replace('[^\w\s]','')
    tweets['text'] = tweets['text'].str.replace('\s+',' ')
    tweets.drop_duplicates(subset = 'text', keep = "first", inplace = True)
    #Merge tweets with copy
    merged = original[original.index.isin(tweets.index)]    

    #Add loanword column
    goodLoanword = word
    #Look up "special" words (macrons/phrases/both) in dictionary
    formatted = {"maori":"māori","non-maori":"non-māori","pakeha":"pākehā","porangi":"pōrangi","haeremai":"haere mai","kiaora":"kia ora","kapahaka":"kapa haka","tenakoutou":"tēnā koutou","kiakaha":"kia kaha","kowhai":"kōwhai","whanau":"whānau","hangi":"hāngī","tereo":"te reo","tane":"tāne","kaimoana":"kai moana","tenakoe":"tēnā koe","korero":"kōrero","powhiri":"pōwhiri","morena":"mōrena","tangatawhenua":"tangata whenua","kakariki":"kākāriki","maui":"mauī","kohanga":"kōhanga","hapu":"hāpu","kaumatua":"kaumātua","kainga":"kāinga","wahitapu":"wāhi tapu","wananga":"wānanga","hikoi":"hīkoi","papatuanuku":"papatūānuku","whangai":"whāngai","mawhero":"māwhero","hoha":"hōhā","kawanatanga":"kāwanatanga","kuri":"kurī"}    
    for loanword in formatted:
        if word in formatted:
            goodLoanword = formatted.get(word, "none")
    merged.insert(0, 'loanword', goodLoanword)
    
    #Reorder columns
    #print(list(merged.columns.values))
    merged = merged[['loanword', 'id', 'text', 'username', 'date','retweets','favourites','geo','mentions','hashtags','permalink']]
    
    #Store in CSV
    outputFile = DIR + "/" + word + "-good.csv"
    #print(outputFile)
    merged.to_csv(outputFile, sep="\t", index = False) 
    #print(tweets)

#Get filepaths for all CSVs in directory
def getFiles(suffix, methodToCall):
    for root, dirs, files in os.walk(DIR, topdown=False):   
        #For each file
        for filename in files:
            #If it's a CSV (containing Tweets)
            if filename.endswith(suffix):
                #Join filename with path to get location
                filePath = os.path.join(root, filename)            
                print("Processing %s..." % filename)
                methodToCall(filePath)
                
def convertAllToTSV():
    getFiles(".csv", cleanTweets)        

def removeAllSimilarTweets():   
    getFiles("-duplicates.csv", removeSimilarTweets)        

#Reads a CSV file containing Tweets
def readCSV(inputFile):
    tweets = []
    with open(inputFile) as csvFile:
        for row in csv.reader(csvFile, delimiter='\n'):
            #For each tweet
            for term in row:
                tweets.append(term)
    return tweets

#Generates a random sample of 200 Tweets or just shuffles Tweets if population < 200.
def getRandomSample(tweets):
    #Don't include header in sample
    header = tweets[0]
    tweets.remove(header)
    SAMPLE_SIZE = 200
    #If there are fewer than 200 tweets
    if(len(tweets) < SAMPLE_SIZE):
        SAMPLE_SIZE = len(tweets)
    sample = random.sample(tweets, SAMPLE_SIZE)
    #Insert header
    sample.insert(0, header)
    return sample

#Save CSV 
def writeToCSV(word, sample):
    #https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python
    if not os.path.exists(DIR + "/new-samples"):
        os.makedirs(DIR + "/new-samples")
    filename = word.replace(DIR, DIR + "/new-samples").replace(".csv","") + "-sample.csv"
    with open(filename, 'w') as f:
        for tweet in sample:
            f.write(tweet + "\n")
    
#Gets filepaths for all CSVs in directory and calls functions to generate a random sample for each one.
def getFilesForSampling():
    for root, dirs, files in os.walk(DIR, topdown=False):   
        #For each file
        for filename in files:
            #If it's a CSV (containing Tweets)
            if filename.endswith("-good.csv"):
                #Join filename with path to get location
                filePath = os.path.join(root, filename)            
                print("Processing %s..." % filename)
                #Read file
                tweets = readCSV(filePath)
                #Generate random sample
                sample = getRandomSample(tweets)
                #Save to file
                writeToCSV(filePath, sample)

convertAllToTSV()
removeAllSimilarTweets()
getFilesForSampling()
print("Done!")