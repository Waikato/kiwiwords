#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#https://www.shanelynn.ie/word-embeddings-in-python-with-spacy-and-gensim/

from gensim.models.phrases import Phrases, Phraser

#Training data
sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
			['this', 'is', 'the', 'second', 'sentence'],
			['yet', 'another', 'sentence'],
			['one', 'more', 'sentence'],
			['and', 'the', 'final', 'sentence']]

#Phrase Detection
#Common terms that can be ignored in phrase detection
#For example, 'state_of_affairs' will be detected because 'of' is provided here: 
common_terms = ["of", "with", "without", "and", "or", "the", "a"]
#Create the relevant phrases from the list of sentences:
phrases = Phrases(all_sentences, common_terms=common_terms)
#The Phraser object is used from now on to transform sentences
bigram = Phraser(phrases)
#Applying the Phraser to transform our sentences is simply
all_sentences = list(bigram[all_sentences])