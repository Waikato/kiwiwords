#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Converts the output of get_tweets_with_bearer_token.py into a TSV file
#Also applies consistent formatting (as described in the RMT Corpus paper)
#e.g. Decodes HTML, removes special characters, standardises user
#mentions and links
#Finally, supplements the data with derived metadata from the file 
#containing the tweet IDs.

import pandas as pa
import re
from string import printable
import html
import os

#Modify the JSON so that there is one tweet (instance) per line
def correct_output(input_file):
    with open(input_file, 'r', encoding="utf8") as f:
        output_file = input_file.replace(".json", "2.json")
        with open(output_file, 'w', encoding="utf8") as writer:
            next(f)
            for line in f:
                #Transform API output to get one object per line
                line = line.replace("[", "")
                line = line.replace("]", "")
                #Strip newline characters 
                line = line.replace("\n", "")
                #Remove commas after "}"
                #Note that this doesn't work for fields which are their own
                #arrays, such as geo information - but this can be easily fixed
                line = line.replace("},", "}\n")
                p = re.compile(r"Batch \d+, Code \d+")
                line = p.sub(r"\n", line)
                line = line.replace('"errors":', "\n")
                print(line, end="", file=writer)
                
#Fix tweets containing speech marks (turn double quotes into single quotes)
def further_correct_output(input_file):
    with open(input_file, 'r', encoding="utf8") as f:
        output_file = input_file.replace("2.json", "3.json")
        with open(output_file, 'w', encoding="utf8") as writer:
            for line in f:
                #If tweet text contains speech marks, change them to single quotes
                p = re.search(r'"text": "(.*)"        }', line)
                group = p.group(1) if p is not None else 'Not found'
                if (group != "Not found"):
                    #print(group)
                    group = group.replace('"',"'")
                    group = group.replace(r"\n", "")
                    #print(group)
                    #Delete text
                    p = re.compile(r'"text": "(.*)"        }')
                    line = p.sub(r'"text": "' + group + '"     }', line)     
                print(line, end="", file=writer)
    
#Extract relevant fields from JSON
def extract_info(input_file):
    with open(input_file, 'r', encoding="utf8") as f:
        output_file = input_file.replace(".json", ".csv")                
        with open(output_file, 'w', encoding="utf8") as writer:
            #Add header to output file
            print("id\ttext\tconversation_id\tin_reply_to_user_id\tauthor_id\tcreated_at\tlang\tsource\terror", file=writer)
            for line in f:
                #Extract tweet ID
                p = re.search(r'"id": "(\d*)"', line)
                tweet_id = p.group(1)+"'" if p is not None else 'Unknown'
                #If there is no "id" property, use the "value" property instead (which is used for errors)
                if (tweet_id == 'Unknown'):
                    p = re.search(r'"value": "(\d*)"', line)
                    tweet_id = p.group(1)+"'" if p is not None else 'Unknown'
                    
                #Update the list of properties as required!
                #Should match properties in get_tweets_with_bearer_token.py
                properties = ["text","conversation_id","in_reply_to_user_id","author_id","created_at","lang","source","title"]
                data = []
                for prop in properties:
                    p = re.search(r'"' + prop + '": "(.*?)"', line)
                    datum = p.group(1) if p is not None else 'None'
                    data.append(datum)
                print(tweet_id + "\t" + "\t".join(data), file=writer) 

def format_data(input_file):
    output_file = input_file.replace("3.csv", "4.csv")
        
    tweets = remove_special_chars(input_file)
    tweets.to_csv(output_file, sep="\t", header = True, index = False)
    
    tweets = decode_html_links(output_file)
    tweets.to_csv(output_file, sep="\t", header = True, index = False)
        
    tweets = standardise_user_mentions(output_file)
    content = tweets.pop("content_with_emojis")
    tweets.insert(2, content.name, content) 
    tweets.to_csv(output_file, sep="\t", header = True, index = False)
    
#Removes emojis and other special characters
def remove_special_chars(inputFile):
    tweets = pa.read_csv(inputFile, sep="\t", lineterminator='\n')
    good_tweets = []
    for tweet in tweets['text']:
        tweet = tweet.replace("\\'","'")
        #Remove emojis
        #permitted_chars = printable + "ĀĒĪŌŪāēīōū" 
        #tweet = "".join(c for c in tweet if c in permitted_chars) 
        #spaces = re.compile(r" {2,}")
        #tweet = spaces.sub(r" ", tweet)
        speechmarks = re.compile(r'"{1,}')
        tweet = speechmarks.sub(r"'", tweet)
        good_tweets.append(tweet)
    #Remove (original) text column
    del tweets['text']
    #Insert new column with decoded text
    tweets['text'] = good_tweets
    return tweets
    
#Decodes all HTML entities in tweet text (e.g. '&lt;' becomes '<')
#TEST: What happens to '&quot;' ??? Replace these?
def decode_html_links(input_file):
    #Run twice to fix tweets like &amp;amp;
    good_tweets = []
    #tweets = pa.read_csv(input_file, sep="\t", skiprows=range(1,114240), nrows=3)    
    tweets = pa.read_csv(input_file, sep="\t")         
    for tweet in tweets['text']:
        #print(tweet)
        decoded = html.unescape(tweet)
        decoded = decoded.replace('"',"'")    
        #Remove pilcrows
        #decoded = decoded.replace("¶ ","")
        #Remove random remaining emojis - ONLY ACCEPT [A-Z,a-z,0-9,macrons,punctuation?]
        #emojis = re.compile(r" ♀️")
        #decoded = emojis.sub(r"", decoded)
        #Standardise URLs (NB: removes any punctuation immediately after link - if no space)
        urls = re.compile(r"http\S*")
        decoded = urls.sub(r"<link>", decoded)
        good_tweets.append(decoded)
    #Remove (original) text column
    del tweets['text']
    #Insert new column with decoded text
    tweets['text'] = good_tweets
    return tweets

def standardise_user_mentions(input_file):
    good_tweets = []
    tweets = pa.read_csv(input_file, sep="\t")         
    for tweet in tweets['text']:
        usernames = re.compile(r"@\S+")
        tweet = usernames.sub(r"<user>", tweet)
        #Correct formula error
        formula_error = re.compile(r"^=")
        tweet = formula_error.sub("", tweet)
        good_tweets.append(tweet)
    del tweets['text']
    tweets['content_with_emojis'] = good_tweets
    
    #CREATE VERSION WITHOUT EMOJIS
    tweets['content'] = tweets['content_with_emojis']
    content = []
    for tweet in tweets['content']:
        permitted_chars = printable + "ĀĒĪŌŪāēīōū" 
        tweet = "".join(c for c in tweet if c in permitted_chars) 
        spaces = re.compile(r" {2,}")
        tweet = spaces.sub(r" ", tweet)
        content.append(tweet)
    del tweets['content']
    tweets['content'] = content
    
    return tweets

#Add derived metadata to the final dataframe
def supplement_data(file1, file2, file3, joinCol):
    #https://www.geeksforgeeks.org/how-to-do-a-vlookup-in-python-using-pandas/
    df1 = pa.read_csv(file1, sep="\t", dtype={'id': 'str'}) 
    df2 = pa.read_csv(file2, sep="\t", dtype={'id': 'str'}) 
    df3 = pa.merge(df1,df2,on=joinCol, how="outer")
    #Sort columns alphabetically
    #df3 = df3.reindex(columns=sorted(df3.columns))
    #Move ID and text columns to front
    first_col = df3.pop("content")
    df3.insert(0, "content", first_col)
    first_col = df3.pop("content_with_emojis")
    df3.insert(0, "content_with_emojis", first_col)
    first_col = df3.pop("id")
    df3.insert(0, "id", first_col)
    df3.to_csv(file3, sep="\t", index=False)
    
def remove_tmp_files():
    tmp_files = ["output2.json", "output3.json", "output3.csv", "output4.csv"]
    for file in tmp_files:    
        try:
            os.remove(file)
        except OSError as e:
            print("Error: %s : %s" % (file, e.strerror))
    
correct_output("output.json")
further_correct_output("output2.json")
extract_info("output3.json")
format_data("output3.csv")
supplement_data("output4.csv","rmt-corpus-v1.csv","rmt-corpus-final.csv","id")
remove_tmp_files()

print("Done!")    
