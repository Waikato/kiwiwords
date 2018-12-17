#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 15:08:36 2018

@author: fbravoma
"""

import glob
import pandas as pa
from gensim.models.phrases import Phrases, Phraser
from gensim.models.word2vec import LineSentence
from gensim.models import Word2Vec
from gensim.models import FastText

from .twokenize import tokenizeRawTweetText


def corpus2plainfile(source,target,extension='csv',col_name='text',sep="\t"):
        """
        converts a folder with csv files into a single file including just the tweet content. 
        Tweets are tokenized with tweetNLP and lowercased.
        One line per tweet.
        """    
       
        
        with open(target, 'a') as out_file:
            #os.chdir(source)
            csv_files = [i for i in glob.glob(source+'/*.{}'.format(extension))]
            print(csv_files)
            for file in csv_files:
                tweets = pa.read_csv(file,sep=sep)
                for tweet in tweets[col_name]:
                    clean_tweet = ' '.join(tokenizeRawTweetText(tweet.lower()))
                    out_file.write(clean_tweet+"\n")





def proc_phrases(source,target):
    """
    runs a PMI-based phrase detector on a corpus of lines.
    Sentences with detected phrases are stored in target.
    """      

    sentences = LineSentence(source)
    
     
    common_terms = ["of", "with", "without", "and", "or", "the", "a"]
    # Create the relevant phrases from the list of sentences:
    phrases = Phrases(sentences, common_terms=common_terms)
    # The Phraser object is used from now on to transform sentences
    bigram = Phraser(phrases)
    with open(target, 'a') as out_file:
        for sentence in bigram[sentences]:
            out_file.write(' '.join(sentence)+"\n")
    
    
    
def train_wordvectors(source,target):
    emb_models=[Word2Vec,FastText]
    window_sizes = [1,2,3,5,10,15]
    vector_dims = [10,50,100,200,400,800]
    min_c = 10
    numWorkers = 20
    
    sentences = LineSentence(source)     
     
    for emb_mod in emb_models:
        model = emb_mod(sentences, min_count=min_c, window = 5, size = 100)
        model.save(target+"-"+model.__class__.__name__+'.bin')
        
       
     
 
 # =============================================================================
 # 
 # for  in windowSizes:
 #     for embeddingS in embeddingSizes:
 #         for corporaName, copora in coporaList:
 #             for modelType in modelList:
 #                 newModel = modelType(copora, size=embeddingS, window=windowS, min_count=minCount, workers=numWorkers)
 #                 modelName = newModel.__class__.__name__+"-"+str(embeddingS)+"-"+str(windowS)+"-"+corporaName
 #                 print(modelName)
 #                 getRankAndOutput(newModel, goldPairs, modelName)
 # =============================================================================
 
 
 
 # train model
# model = FastText(sentences, min_count=1, window = 5, size = 100)
# # summarize the loaded model
# print(model)
# # summarize vocabulary
# words = list(model.wv.vocab)
# print(words)
# # access vector for one word
# print(model['sentence'])
# # save model
# model.save('model.bin')
# # load model
# new_model = Word2Vec.load('model.bin')
# print(new_model)

    
    
    
