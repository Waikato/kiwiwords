#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 11:44:49 2018

@author: fbravoma
"""
from gensim.models import Word2Vec
from gensim.models import FastText
from gensim.test.utils import datapath
from gensim.models.phrases import Phrases, Phraser
from gensim.models.word2vec import LineSentence
from embeddings.functions import corpus2plainfile
import argparse


parser = argparse.ArgumentParser(description='Process Maori Loandwords tweets and train embeddings')

parser.add_argument('--corpus_path', type=str, default="data",
                    help='Path to the corpus folder',
                    metavar='')


parser.add_argument('--master_file', type=str, default="masterTweets.txt",
                    help='Name of processed corpus',
                    metavar='')


parser.add_argument('--process_corpus', action='store_true',
                    help='Process corpus')


args = parser.parse_args()

if args.process_corpus:
    corpus2plainfile(args.corpus_path,args.master_file)     

# =============================================================================
# 
# 
# sentences = LineSentence("../embeddings/masterTweets.txt")
# 
# common_terms = ["of", "with", "without", "and", "or", "the", "a"]
# # Create the relevant phrases from the list of sentences:
# phrases = Phrases(sentences, common_terms=common_terms)
# # The Phraser object is used from now on to transform sentences
# bigram = Phraser(phrases)
# # Applying the Phraser to transform our sentences is simply
# all_sentences = list(bigram[sentences])
# 
# 
# emb_models=[Word2Vec,FastText]
# window_sizes = [1,2,3,5,10,15]
# vector_dims = [10,50,100,200,400,800]
# min_c = 10
# numWorkers = 20
# 
# 
# for emb_mod in emb_models:
#     model = emb_mod(sentences, min_count=min_c, window = 5, size = 100)
#     print(model)
#     words = list(model.wv.vocab)
#     print(words)
#     
# 
# # =============================================================================
# # 
# # for  in windowSizes:
# #     for embeddingS in embeddingSizes:
# #         for corporaName, copora in coporaList:
# #             for modelType in modelList:
# #                 newModel = modelType(copora, size=embeddingS, window=windowS, min_count=minCount, workers=numWorkers)
# #                 modelName = newModel.__class__.__name__+"-"+str(embeddingS)+"-"+str(windowS)+"-"+corporaName
# #                 print(modelName)
# #                 getRankAndOutput(newModel, goldPairs, modelName)
# # =============================================================================
# 
# 
# 
# # train model
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
# =============================================================================
