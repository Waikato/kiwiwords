#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pa
import re

"""Script to calculate frequencies of all hashtags in the RMT Corpus.
Hashtags with macrons and capital letters are consolidated with hashtags
without macrons and lower-case letters."""

#Extract ALL hashtags and report how many times they occur each year.   
def get_hashtag_frequencies(input_file):
    table_rows = []
    table_rows.append("hashtag\tnum_tweets\tnum_appearances\t2007\t2008\t2009\t2010\t2011\t2012\t2013\t2014\t2015\t2016\t2017\t2018\t2019\t2020\tUnknown\tdistinct_users\n")
    tweets = pa.read_csv(input_file, sep="\t")
    #Convert text to lowercase
    tweets['content'] = tweets['content'].str.lower()
    #Remove macrons
    tweets['content'] = tweets['content'].apply(lambda x: re.sub("ā","a", x))
    tweets['content'] = tweets['content'].apply(lambda x: re.sub("ē","e", x))
    tweets['content'] = tweets['content'].apply(lambda x: re.sub("ī","i", x))
    tweets['content'] = tweets['content'].apply(lambda x: re.sub("ō","o", x))
    tweets['content'] = tweets['content'].apply(lambda x: re.sub("ū","u", x))
    #Extract all hashtags
    hashtags = dict(tweets['content'].str.extractall(r"(\#\w+)")[0].value_counts())
    for h, v in hashtags.items():
        #print(h)
        #print(v)
        #Don't count sub-hashtags (e.g. #kiwis doesn't count #kiwi)
        tweets_containing_hashtag = tweets[tweets['content'].str.contains(h + r'[ ,.#!)@?]')|tweets['content'].str.endswith(h)]
        users = len(tweets_containing_hashtag['user.id'].unique())
        counts = get_year_counts(tweets_containing_hashtag)
        total = sum(counts.values())
        #print(total)
        final = pa.DataFrame([counts.values()]).to_string(header=False, index=False).replace("  ", "\t")
        table_rows.append(h + "\t" + str(total) + "\t" + str(v) + "\t" + final + "\t" + str(users) + "\n")    
    #Write to file
    output_file = "rmt-diachronic-hashtags.csv"    
    with open(output_file, 'w', encoding='utf-8') as f:
        for t in table_rows:
            f.write(t)
            
def get_year_counts(tweets):
    #y_keys = tweets['year'].unique().tolist()
    y_keys = ["2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019","2020","Unknown"]
    tweets['year'] = tweets['year'].astype(str)
    y_values = []
    index = 0
    for year in y_keys:
        count = len(tweets[tweets['year'].str.contains(year)])
        y_values.insert(index, count)
        index+=1
    year_counts = dict(zip(y_keys, y_values))
    return year_counts

##########################################################################
            
#Calculate diachronic frequences for GIVEN hashtags only    
def get_selected_hashtag_frequencies(input_file):
    tweets = pa.read_csv(input_file, sep="\t")
    table_rows = []
    #table_rows.append("hashtag\tnum_tweets\t2007\t2008\t2009\t2010\t2011\t2012\t2013\t2014\t2015\t2016\t2017\t2018\tdistinct_users\n")
    hashtags = pa.read_csv("selected-hashtags.csv")
    selected_hashtags = list(hashtags['hashtag'])   
    #hashtags = selected_hashtags.sort()
    for hashtag in selected_hashtags:
        hashtag = hashtag.lower()
        hashtag = hashtag.replace("ā","a")
        #tweets_containing_hashtag = tweets[tweets['text'].str.contains(hashtag + r'[ ,.#!)@?]')|tweets['text'].str.endswith(hashtag)]
        tweets_containing_hashtag = tweets[tweets['hashtag'].str.match(re.compile(hashtag + r"$"))]
        print(hashtag)
        #users = len(tweets_containing_hashtag['username'].unique())
        counts = get_month_counts(tweets_containing_hashtag)
        total = sum(counts.values())
        final = pa.DataFrame([counts.values()]).to_string(header=False, index=False).replace("  ", "\t")
        table_rows.append(hashtag + "\t" + str(total) + "\t" + final + "\n")    
        #Write to file
    output_file = "monthly-diachronic-hashtag-frequencies.csv"    
    with open(output_file, 'w') as f:
        for t in table_rows:
            f.write(t)

def get_month_counts(tweets):
    months = pa.read_csv("all-months.csv", sep="\t")
    m_keys = months['month'].unique().tolist()
    m_values = []
    index = 0
    for year in m_keys:
        count = len(tweets[tweets['timestamp'].str.contains(year)])
        m_values.insert(index, count)
        index+=1
    month_counts = dict(zip(m_keys, m_values))
    return month_counts  

##########################################################################
        
get_hashtag_frequencies("rmt-corpus-v1.csv")
print("Done!")