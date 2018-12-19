#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 11:44:49 2018

@author: fbravoma
"""

from embeddings.functions import corpus2plainfile, proc_phrases, train_wordvectors, eval_embeddings, t_sne_scatterplot
import argparse


parser = argparse.ArgumentParser(description='Process Maori Loandwords tweets and train embeddings')



parser.add_argument('--proc_corpus', action='store_true',
                    help='Process corpus')


parser.add_argument('--corpus_path', type=str, default="data/rawtweets",
                    help='Path to the corpus folder',
                    metavar='')


parser.add_argument('--tweet_outfile', type=str, default="all_tweets.txt",
                    help='Name of processed corpus',
                    metavar='')


parser.add_argument('--proc_phrases', action='store_true',
                    help='Extract phrases')

parser.add_argument('--phrase_outfile', type=str, default="all_tweets_phrases.txt",
                    help='Name of processed corpus after detecting phrases',
                    metavar='')


parser.add_argument('--train_wordvectors', action='store_true',
                    help='Train word vectors')



parser.add_argument('--eval_wordvectors', action='store_true',
                    help='Evaluate word vectors')




parser.add_argument('--plot_wordvectors', action='store_true',
                    help='Plot word vectors')


args = parser.parse_args()

if args.proc_corpus:
    corpus2plainfile(args.corpus_path,args.tweet_outfile)   
    
    
if args.proc_phrases:
     proc_phrases(args.tweet_outfile,args.phrase_outfile)

if args.train_wordvectors:
    train_wordvectors('all_tweets_phrases.txt','experiments')
    
if args.eval_wordvectors:
    eval_embeddings('experiments','data/gold_pairs.csv','emb_res.csv')
    
if args.plot_wordvectors:
    t_sne_scatterplot()
    