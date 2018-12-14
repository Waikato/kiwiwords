#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import csv
import numpy
import nltk
import matplotlib.pyplot as plt
from gensim.models import Word2Vec
from gensim.models import FastText
from sklearn.manifold import TSNE
from wordcloud import WordCloud
#%%
def testing(outputListMaori, outputListMixed, goldPairs):
    coporaList=[("maori", outputListMaori),("mixed", outputListMixed)]
    modelList=[Word2Vec,FastText]
    windowSizes = [1,2,3,5,10,15]
    embeddingSizes = [10,50,100,200,400,800]
    minCount = 10
    numWorkers = 20
    #notFoundWords = ["koutou","kaore","pakeha","urupa"]
    
    for windowS in windowSizes:
        for embeddingS in embeddingSizes:
            for corporaName, copora in coporaList:
                for modelType in modelList:
                    newModel = modelType(copora, size=embeddingS, window=windowS, min_count=minCount, workers=numWorkers)
                    modelName = newModel.__class__.__name__+"-"+str(embeddingS)+"-"+str(windowS)+"-"+corporaName
                    print(modelName)
                    getRankAndOutput(newModel, goldPairs, modelName)

#%% Given a dictionary of pairs, get the ranking of each of the pairs for the model, return total, ignore if pair isn't found
def getRankAndOutput(newModel, goldPairs, modelName):
    with open('totalRanks.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        totalRank = 0
        for k,v in goldPairs.items():
            try:
                print("(" + k + "," + v + ")"+str(newModel.wv.rank(k,v)))
                totalRank += newModel.wv.rank(k,v)
                spamwriter.writerow([str(k)] + [str(v)] + [str(newModel.wv.rank(k,v))] + [str(modelName)])
            except:
                print("pair not found:"+k+","+v)
        return totalRank
#%%
def caseStudyTesting(wordsList, modelType, embeddingS, windowS, corpusList, corpusName, minCount, numWorkers):
    model = modelType(corpusList, size=embeddingS, window=windowS, min_count=minCount, workers=numWorkers)
    with open('similaritiesCaseStudy.csv', 'a+') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for trackWord in wordsList:
            simList = model.wv.most_similar(trackWord, topn=10)
            spamwriter.writerow([model.__class__.__name__]+[corpusName]+[str(embeddingS)]+[str(windowS)]+simList)
#%%
def corpusStats(listToAnalyse):
    numTweets = 0
    numWords = 0
    for tweets in listToAnalyse:
        numTweets += 1
        for words in tweets:
            numWords += 1
    print("Tweet Count: " + str(numTweets))
    print("Word Count:" + str(numWords))
#%%
def hitRateTesting(outputListMaori, outputListMixed, goldPairs, negativePairs):
    coporaList=[("maori", outputListMaori),("mixed", outputListMixed)]
    modelList=[Word2Vec,FastText]
    windowSizes = [1,2,3,5,10,15]
    embeddingSizes = [10,50,100,200,400,800]
    minCount = 10
    numWorkers = 20
    #notFoundWords = ["koutou","kaore","pakeha","urupa"]
    
    for windowS in windowSizes:
        for embeddingS in embeddingSizes:
            for corporaName, copora in coporaList:
                for modelType in modelList:
                    newModel = modelType(copora, size=embeddingS, window=windowS, min_count=minCount, workers=numWorkers)
                    modelName = newModel.__class__.__name__+"-"+str(embeddingS)+"-"+str(windowS)+"-"+corporaName
                    #print(modelName)
                    with open('posNegModelResults.csv', 'a+') as csvfile:
                        spamwriter = csv.writer(csvfile, delimiter=',')
                        totalPositive = calcSimilaritiesModel(newModel, goldPairs)
                        totalNegative = calcNegativeModel(newModel, negativePairs)
                        print(modelName+" "+str(totalPositive-totalNegative))
                        spamwriter.writerow([str(modelName)]+[str(totalPositive-totalNegative)]+[str(totalPositive)]+[str(totalNegative)])
						
#%%https://labsblog.f-secure.com/2018/01/30/nlp-analysis-of-tweets-using-word2vec-and-t-sne/
def t_sne_scatterplot(model, word, file_params):
  vocab = list(model.wv.vocab.keys())
  dim0 = model.wv[vocab[0]].shape[0]
  arr = numpy.empty((0, dim0), dtype='f')
  w_labels = [word]
  nearby = model.wv.similar_by_word(word, topn=50)
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
 
  plt.rc("font", size=16)
  plt.figure(figsize=(16, 12), dpi=80)
  plt.scatter(x_coords[0], y_coords[0], s=800, marker="o", color="blue")
  plt.scatter(x_coords[1:], y_coords[1:], s=200, marker="o", color="red")
 
  for label, x, y in zip(w_labels, x_coords, y_coords):
    plt.annotate(label.upper(), xy=(x, y), xytext=(0, 0), textcoords='offset points')
  plt.xlim(x_coords.min()-50, x_coords.max()+50)
  plt.ylim(y_coords.min()-50, y_coords.max()+50)
  filename = os.path.join(file_params + "_" + word + "_tsne.png")
  plt.savefig(filename)
  plt.close()
  
#%%
def drawWordCloud(dictList):
    wordcloud = WordCloud().generate_from_frequencies(dictList)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
	
#%% Given a line of tokens, get POS tag using nltk, and return as a list
def posLine(lineTokensList):
    linePOSList = nltk.pos_tag(lineTokensList)
    return linePOSList