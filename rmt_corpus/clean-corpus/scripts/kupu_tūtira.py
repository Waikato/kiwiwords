#!/usr/bin/python3
# Returns a list of all Māori words 
#Tells the user what percentage of words are considered 'english' or 'māori'

import re
import os
import sys
import argparse
import string
import pandas as pa
from twokenize import tokenizeRawTweetText
from taumahi import kōmiri_kupu, nahanaha

#Get current directory
DIR = os.path.dirname(os.path.realpath(__file__))

#Returns the plain tweet text from the input file in a single string.
def tangohia_kupu_tōkau(kōwhiri):
    tweets = pa.read_csv(kōwhiri.input, sep="\t", lineterminator='\n')
    text = ' '.join(tweets["content"]).lower()
    #print(text)
    return text

#Writes the list of Māori words to the given file, one word per line.
#If no file is specified, outputs Māori words to the terminal instead.
def tuhi_puta_tuhinga(kōwhiri, kupu_hou):
    #If output file specified
    if kōwhiri.output:
        #Write to output file
        kupu_tūtira_hou = open(kōwhiri.output, "w")
        kupu_tūtira_hou.write("\n".join(kupu_hou))
        kupu_tūtira_hou.close()
    else:
        print(kupu_hou)

def matua():

    #Set up terminal arguments
    whakatukai = argparse.ArgumentParser()
    whakatukai.add_argument(
        '--input', '-i', help="Input multilanguage corpus text file")
    whakatukai.add_argument(
        '--output', '-o', help="Output text file where words that are considered to be Māori are stored")
    kōwhiri = whakatukai.parse_args()
    
    #Gather text from input files
    kupu_tōkau = tangohia_kupu_tōkau(kōwhiri)

    #Writes these words that are considered to be Māori in the text (the keys
    # of the first object returned by the kōmiri_kupu function) to their output
    # files or prints them to the console depending on user input, in Māori
    # alphabetical order
    tuhi_puta_tuhinga(kōwhiri, nahanaha(kōmiri_kupu(kupu_tōkau)[0].keys()))
    
    #Store the Maori words in a list
    #a, i, he, me, to - not counted but more common in English
    maori_words = ['ā','ae','ana','au','e','ia','ka','ki','kia','ko','ma','moe','o','ora','ra','u']
    with open(kōwhiri.output, 'r') as f:
        for line in f:
            maori_words.append(line.strip("\n").lower())
    print(maori_words)
        
    #Reads in a dataframe with multiple columns, but only analyses the tweet text
    tweets = pa.read_csv(kōwhiri.input, sep="\t", lineterminator='\n')
          
    #RUN ON TEMIHINGA AS A TEST?
    #CAN TWEAK THE MAORI WORD LIST ACCORDINGLY
    
    maori_percentages = []    
    #2D array to keep track of Maori words in each tweet
    matches2 = []
    total_words_list = []
    num_maori_words_list = []
    for tweet in tweets["content"]:
        #Remove <link>, <user>, punctuation and unnecessary spaces
        tweet2 = tweet.lower()
        tweet2 = re.sub("<link>", "", tweet2)
        tweet2 = re.sub("<user>", "", tweet2)
        tweet2 = re.sub('['+string.punctuation+']', '', tweet2)
        #tweet = re.sub('\d','',tweet)
        tweet2 = re.sub(r'^ ','',tweet2)
        tweet2 = re.sub(r' $','',tweet2)
        tweet2 = re.sub(r" {2,}", " ", tweet2)
        #print(tweet2)
        #Extract the tokens from the tweet
        tokens = tokenizeRawTweetText(str(tweet2).lower())
        #Store the length of the tweet
        total_words = len(tokens)
        #Counter variable
        num_maori_words = 0
        #List to store all words that are detected as Maori in the tweet
        matches = []
        #For each word in the tweet
        for token in tokens:
            #If the word is also in the list of Maori words
            if token in maori_words:
                #Increment the count
                #print(token)
                matches.append(token)
                num_maori_words += 1
        if(total_words == 0):
            percentage_maori = 0
        else:
            percentage_maori = float(num_maori_words/total_words)
            percentage_maori = round(percentage_maori, 2)
        matches2.append(matches)        
        maori_percentages.append(percentage_maori)
        num_maori_words_list.append(num_maori_words)
        total_words_list.append(total_words)
    #Insert new columns
    tweets['maori_words'] = matches2
    tweets['num_maori_words'] = num_maori_words_list
    tweets['total_words'] = total_words_list
    tweets['percent_maori'] = maori_percentages
    outputFile = kōwhiri.input.replace(DIR + "/", "").replace(".csv", "-percentages.csv")
    tweets.to_csv(outputFile, sep="\t", header = False, index = False)             
            
    #maori_tweets = tweets.loc[tweets['percent_maori'] > 0.5]
    maori_tweets = tweets.loc[((tweets['total_words'] <= 6) & (tweets['percent_maori'] >= 0.8)) | ((tweets['total_words'] > 6) & (tweets['percent_maori'] >= 0.7))]
    
    #Append Maori tweets to file
    maori_tweets.to_csv("maori-tweets.csv", mode="a", sep="\t", header = False, index = False)             
        
if __name__ == '__main__':
    matua()