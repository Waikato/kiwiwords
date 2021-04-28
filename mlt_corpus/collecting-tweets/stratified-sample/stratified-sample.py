#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#One file per loanword
#tweets = num_lines
#rel = relevant/tweets

import pandas as pa

def get_stratified_sample(inputFile):
    #Size of test partition (training is 1-size)
    test_size = 0.2
    #Read the given CSV
    tweets = pa.read_csv(inputFile, sep="\t")
    #Avoid rounding id's when merging
    tweets['id'] = tweets['id'].apply("int64")
    
    counts = dict(tweets['loanword'].value_counts())
    #print(counts)
    
    #DO THIS FOR EACH LOANWORD! replace "tena koutou" with k parsed as string
    
    for l in counts:
        print("Processing " + l + "...")
        total = counts[l]
        num_rel = len(tweets[(tweets['loanword'] == l) & (tweets['relevance'] == "relevant")])
        rel = tweets[(tweets['loanword'] == l) & (tweets['relevance'] == "relevant")]
        non = tweets[(tweets['loanword'] == l) & (tweets['relevance'] == "non-relevant")]
        prop_rel = num_rel/total
        prop_non = 1-prop_rel
        rel_to_sample = int(round(test_size * prop_rel * total))
        non_to_sample = int(round(test_size * prop_non * total))        
        test_rel = rel.sample(n=rel_to_sample, replace=False)
        if non_to_sample > 0:
            test_non = non.sample(non_to_sample, replace=False)
            test = pa.concat([test_rel, test_non])    
        if non_to_sample == 0:
            test = test_rel
        train = tweets.drop(test.index)            
        #Concatenate all
        test.to_csv("test-" + l + ".csv", sep="\t", index = False) 
        train[(train['loanword'] == l)].to_csv("train-" + l + ".csv", sep="\t", index = False)
        
    #random.seed(1)

def remove_headers(inputFile):
    goodTweets = []
    #Read file
    with open(inputFile, 'r') as f:
        for line in f:            
            header = "loanword\tid\tusername\tdate\ttext\trelevance"
            if header not in line:
                goodTweets.append(line)
    #Write to file    
    with open("test-good.csv", 'w') as f:
        for tweet in goodTweets:
            f.write(tweet)
            
def change_delimiter(inputFile):
    #Read the given CSV
    tweets = pa.read_csv(inputFile, sep="\t")
    #Save to output file
    tweets = tweets[['id','username','date','loanword','text','relevance']]
    tweets.to_csv("test.csv", sep=",", index = False)
               
#get_stratified_sample("data.tsv")
#remove_headers("test.csv")
change_delimiter("test-good.csv")
print("Done!")

