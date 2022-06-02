#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 20:05:39 2022

@author: laixu
"""

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk.corpus
import os
import pandas as pd
import numpy as np
import itertools
from matplotlib import pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
stopset = list(set(stopwords.words('english')))

os.chdir('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/')
data_path  = './dataset/'
reddit_df_labeled = pd.read_csv(data_path + 'text_and_label.csv')
sentiment_mapper = {'Negative':-1,
                    'Neutral':0,
                    'Positive':1}

reddit_df_labeled['score'] = reddit_df_labeled['label'].map(sentiment_mapper)

# split train data as 70% 30%
X = reddit_df_labeled['title']
y = reddit_df_labeled['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


def word_feats(words):
    return dict([(word, True) for word in words.split() if word not in stopset])

def get_word_feats_all(input_message, labels):
#for i in range(len(reddit_df_labeled)):
    trainfeats  = []
    for i in range(len(input_message)):
        scentence_word_feats = [(word_feats(w), labels.iloc[i]) for w in [input_message.iloc[i]]]
        trainfeats += scentence_word_feats 
    return trainfeats


trainfeats = get_word_feats_all(X_train,y_train)
        
classifier = NaiveBayesClassifier.train(trainfeats)

predicted_y_list = []
for i in range(len(X_test)):

    predicted_y   = classifier.classify(word_feats(X_test.iloc[i]))
    predicted_y_list.append(predicted_y)
    
validation_y_list = y_test.values.tolist()
true_prediction = np.sum([l1==l2 for l1, l2 in zip(predicted_y_list,validation_y_list)])
accuracy_rate    = true_prediction/len(y_test)
print("accuracy_rate ",accuracy_rate)

# naive bayes on stock direction
# match the ticker on that day with
ticker_location         = pd.read_csv('./dataset/' + 'ticker_location.csv')
ticker_location         = ticker_location.dropna(how = 'any')
ticker_location      = ticker_location.apply(lambda x:x.Ticker.replace("{'",'').replace("'}",'').replace("', '",' '),axis =1)
post_and_ticker       = pd.concat([reddit_df_labeled,ticker_location],axis =1).set_index('timestamp')
# replace Y with stock returns
def stock_return_mapper():
    for i in range(len(ticker_location)):
    ticker_list  = ticker_location.iloc[i].split(' ')
    for ticker in ticker_list:
        posttime     = post_and_ticker.index[i]
        ret          = 

X = reddit_df_labeled['title']
y = reddit_df_labeled['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

