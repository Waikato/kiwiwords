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
from statistics import median

from .twokenize import tokenizeRawTweetText



import numpy
import os
import re
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE



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
    """
    Trains word vectors using various parameters
    """      
    emb_models=[Word2Vec,FastText]
    window_sizes = [1,2,3,5,10,15]
    vector_dims = [10,50,100,200,400,800]
    min_c = 10
#    numWorkers = 20
    
    sentences = LineSentence(source)     
     
    for w in window_sizes:
        for v_dim in vector_dims:
            for emb_mod in emb_models:
                model = emb_mod(sentences, min_count=min_c, window = w, size = v_dim)
                model.save(target+"/"+model.__class__.__name__+'-w'+str(w)+"-d"+str(v_dim)+'.bin')
        
       
     


def eval_embeddings(model_folder, gold_pairs, target):
    """
    Evaluates word embeddings
    """ 
    
    
    model_folder = 'experiments'
    gold_pairs = 'data/gold_pairs.csv'
    
    pairs = pa.read_csv(gold_pairs,sep='\t')
    
    model_files = [i for i in glob.glob(model_folder+'/*.{}'.format("bin"))]
    
    
    with open(target, 'a') as out_file:
        out_file.write("model\tw_value\td_value\tmedian.rank\n")
    
        for model_file in model_files:    
            print(model_file)
            model = Word2Vec.load(model_file)
            ranks = []
            for index, row in pairs.iterrows():
                eng,mao = row['English'], row['Te Reo Maori']
                if eng in model.wv.vocab and mao in model.wv.vocab:
                    ranks.append(model.wv.rank(eng,mao))
            
            try:
                w_pattern = re.search('-w(.+?)-', model_file)
                w_value = w_pattern.group(1)
                
                d_pattern = re.search('-d(.+?)\.bin', model_file)
                d_value = d_pattern.group(1)
                
                
                out_file.write(model_file[:model_file.find('-')]+"\t"+str(w_value)+"\t"+str(d_value)+"\t"+str(median(ranks))+"\n")
            except:
                continue
    
  
    


 
def t_sne_scatterplot(model_file = "experiments/Word2Vec-w5-d200.bin", words = ['marae','kia_ora','whanau','wahine','hapu','kura','haka','kiwi','whakapapa','kia_kaha','matariki','aroha'], target = "pics"):
    """
    plots word vectors
    """ 
    
    model = Word2Vec.load(model_file)
    
    for word in words:   
        vocab = list(model.wv.vocab.keys())
        dim0 = model.wv[vocab[0]].shape[0]
        arr = numpy.empty((0, dim0), dtype='f')
        w_labels = []
        
        w_labels.append(word)
        nearby = model.wv.similar_by_word(word, topn=40)
        arr = numpy.append(arr, numpy.array([model[word]]), axis=0)
        for n in nearby:
            w_vec = model[n[0]]
            w_labels.append(n[0])
            arr = numpy.append(arr, numpy.array([w_vec]), axis=0)
     
        tsne = TSNE(n_components=2, random_state=1)
        numpy.set_printoptions(suppress=True)
        Y = tsne.fit_transform(arr)
        x_coords = Y[:, 0]
        y_coords = Y[:, 1]
         
        plt.rc("font", size=9)
        plt.figure(figsize=(16, 12), dpi=80)
        plt.scatter(x_coords[0], y_coords[0], s=800, marker="o", color="blue")
        plt.scatter(x_coords[1:], y_coords[1:], s=200, marker="o", color="red")
     
        for label, x, y in zip(w_labels, x_coords, y_coords):
            plt.annotate(label.upper(), xy=(x, y), xytext=(0, 0), textcoords='offset points')
      
        plt.xlim(x_coords.min()-50, x_coords.max()+50)
        plt.ylim(y_coords.min()-50, y_coords.max()+50)
        filename = os.path.join(target+"/"+word+"_tsne.png")
        plt.savefig(filename)
        plt.close()
    
    
    
