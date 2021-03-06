#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 20:05:39 2022

@author: laixu
"""
import os
os.chdir('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/')
import nltk
import preprocess
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
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import stopwords
import re
stopset = list(set(stopwords.words('english')))


data_path  = './dataset/'
reddit_df_labeled = pd.read_csv(data_path + 'text_and_label.csv')
sentiment_mapper = {'Negative':-1,
                    'Neutral':0,
                    'Positive':1}

reddit_df_labeled['score'] = reddit_df_labeled['label'].map(sentiment_mapper)


def get_preprocessed(data):
    processed = preprocess.get_processed_data(data)
    dict_titles = preprocess.convert_to_dict(processed,"title")
    filtered_titles = preprocess.remove_stop_words(dict_titles)
    return filtered_titles

# split train data as 90% 10%
X = reddit_df_labeled
processed = preprocess.get_processed_data(reddit_df_labeled)
dict_titles = preprocess.convert_to_dict(processed,"title")
filtered_titles = preprocess.remove_stop_words(dict_titles)


# split train data as 70% 30%
X = pd.Series(filtered_titles.values())

y = reddit_df_labeled['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)


def word_feats(words):
    return dict([(word, True) for word in words if word not in stopset])

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

train_y_predicted_list = []
for i in range(len(X_train)):

    train_y_predicted   = classifier.classify(word_feats(X_train.iloc[i]))
    train_y_predicted_list.append(train_y_predicted)
    
validation_y_train_list = y_train.values.tolist()
true_prediction = np.sum([l1==l2 for l1, l2 in zip(train_y_predicted_list,validation_y_train_list)])
accuracy_rate    = true_prediction/len(y_train)
print("accuracy_rate train ",accuracy_rate)
classifier.show_most_informative_features(15)



# naive bayes on stock direction
# match the ticker on that day with
open2open_ret            = pd.read_csv('./dataset/open2open_ret.csv', index_col =0)
ticker_location          = pd.read_csv('./dataset/' + 'ticker_location.csv')
ticker_location         = ticker_location.dropna(how = 'any')
ticker_location         = ticker_location.apply(lambda x:x.Ticker.replace("{'",'').replace("'}",'').replace("', '",' '),axis =1)
post_and_ticker          = pd.concat([reddit_df_labeled,ticker_location],axis =1).set_index('timestamp')
post_and_ticker.index   = pd.to_datetime(post_and_ticker.index)
post_and_ticker.index   = post_and_ticker.index.map(lambda x: datetime.strftime(x, '%Y-%m-%d'))

# replace Y with stock returns
def stock_return_mapper(ticker_location, input_ret, post):
    posttime_list    = []
    ticker_ret_list  = []
    for i in range(len(ticker_location)):
        ticker_list  = ticker_location.iloc[i].split(' ')
        post_i       = post.iloc[ticker_location.index[i]]['title']
    
        for ticker in ticker_list:
           posttime     =post.iloc[ticker_location.index[i]].name
           posttime_1d_later    = pd.to_datetime(posttime) + timedelta(1)
           posttime    = datetime.strftime(posttime_1d_later,'%Y-%m-%d')
           if posttime in input_ret.index:
               ticker_ret   = input_ret.loc[posttime,ticker]
               posttime_list.append(post_i)
               ticker_ret_list.append(ticker_ret)
    return posttime_list,ticker_ret_list
posttime_list,ticker_ret_list  = stock_return_mapper(ticker_location, open2open_ret , post_and_ticker)


def stock_return_mapper_with_preprocessing(ticker_location, input_ret, post_dict, post):
    posttime_list    = []
    ticker_ret_list  = []
    for i in range(len(ticker_location)):
        ticker_list  = ticker_location.iloc[i].split(' ')
        post_i       = post_dict[i]
    
        for ticker in ticker_list:
           posttime     =post.iloc[ticker_location.index[i]].name
           posttime_1d_later    = pd.to_datetime(posttime) + timedelta(1)
           posttime    = datetime.strftime(posttime_1d_later,'%Y-%m-%d')
           if posttime in input_ret.index:
               ticker_ret   = input_ret.loc[posttime,ticker]
               posttime_list.append(post_i)
               ticker_ret_list.append(ticker_ret)
    return posttime_list,ticker_ret_list
posttime_list,ticker_ret_list  = stock_return_mapper_with_preprocessing(ticker_location, open2open_ret , X, post_and_ticker)

#ret_na_len               = len(post_and_ticker.index[post_and_ticker.index =='2021-01-28'])
ticker_ret_direction     = [1 if x >0 else -1 if x<0 else 0 for x in ticker_ret_list]

#X = pd.Series(posttime_list[ret_na_len:])
#y = pd.Series(ticker_ret_direction[ret_na_len:])

X = pd.Series(posttime_list)
y = pd.Series(ticker_ret_direction)

train_test_split   = 0.8
train_len          = round(train_test_split * len(y))


X_train    = X.iloc[:train_len,]
y_train    = y.iloc[:train_len]
X_test     = X.iloc[train_len:,]
y_test     = y.iloc[train_len:,]

trainfeats = get_word_feats_all(X_train,y_train)
        
classifier = NaiveBayesClassifier.train(trainfeats)

predicted_y_list = []
for i in range(len(X_test)):

    predicted_y   = classifier.classify(word_feats(X_test.iloc[i]))
    predicted_y_list.append(predicted_y)
    
validation_y_list = y_test.values.tolist()
true_prediction = np.sum([l1==l2 for l1, l2 in zip(predicted_y_list,validation_y_list)])
accuracy_rate    = true_prediction/len(y_test)
print("accuracy_rate test ",accuracy_rate)

train_y_predicted_list = []
for i in range(len(X_test)):

    train_y_predicted   = classifier.classify(word_feats(X_train.iloc[i]))
    train_y_predicted_list.append(train_y_predicted)
    
validation_y_train_list = y_train.values.tolist()
true_prediction = np.sum([l1==l2 for l1, l2 in zip(train_y_predicted_list,validation_y_train_list)])
accuracy_rate    = true_prediction/len(y_train)
print("accuracy_rate train ",accuracy_rate)
classifier.show_most_informative_features(15)


high_corr_tickers  = ['GME','NOK','AMC','SNDL','CRSR','NOK','MVIS','AAL']
def stock_return_mapper_high_corr_tickers(ticker_location, input_ret, post, high_corr_tickers):
    posttime_list    = []
    ticker_ret_list  = []
    for i in range(len(ticker_location)):
        ticker_list  = ticker_location.iloc[i].split(' ')
        post_i       = post.iloc[ticker_location.index[i]]['title']
    
        for ticker in ticker_list:
            if ticker in high_corr_tickers :
                posttime     =post.iloc[ticker_location.index[i]].name
                posttime_1d_later    = pd.to_datetime(posttime) + timedelta(1)
                posttime    = datetime.strftime(posttime_1d_later,'%Y-%m-%d')
                if posttime in input_ret.index:
                    ticker_ret   = input_ret.loc[posttime,ticker]
                    posttime_list.append(post_i)
                    ticker_ret_list.append(ticker_ret)
    return posttime_list,ticker_ret_list
posttime_list,ticker_ret_list  = stock_return_mapper_high_corr_tickers(ticker_location, open2open_ret , post_and_ticker,high_corr_tickers )

ret_na_len               = len(post_and_ticker.index[post_and_ticker.index =='2021-01-28'])
ticker_ret_direction     = [1 if x >0 else -1 if x<0 else 0 for x in ticker_ret_list]

#X = pd.Series(posttime_list[ret_na_len:])
#y = pd.Series(ticker_ret_direction[ret_na_len:])
X = pd.Series(posttime_list)
y = pd.Series(ticker_ret_direction)
train_test_split   = 0.8
train_len          = round(train_test_split * len(y))


X_train    = X.iloc[:train_len,]
y_train    = y.iloc[:train_len]
X_test     = X.iloc[train_len:,]
y_test     = y.iloc[train_len:,]

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

train_y_predicted_list = []
for i in range(len(X_test)):

    train_y_predicted   = classifier.classify(word_feats(X_train.iloc[i]))
    train_y_predicted_list.append(train_y_predicted)
    
validation_y_train_list = y_train.values.tolist()
true_prediction = np.sum([l1==l2 for l1, l2 in zip(train_y_predicted_list,validation_y_train_list)])
accuracy_rate    = true_prediction/len(y_train)
print("accuracy_rate train ",accuracy_rate)
classifier.show_most_informative_features(15)