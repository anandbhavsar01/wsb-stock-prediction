#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  4 20:37:16 2022

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
os.chdir('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/')
data_path  = './dataset/'
reddit_df = pd.read_csv(data_path + 'reddit_wsb.csv')



text= reddit_df['title'][1]
tokenized_text=sent_tokenize(text)
token = word_tokenize(tokenized_text[0])
token

a = set(stopwords.words('english'))
sid_obj = SentimentIntensityAnalyzer()

def sentiment_scores(sentence):
# Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
# polarity_scores method of SentimentIntensityAnalyzer
# oject gives a sentiment dictionary.
# which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)
    print("Overall sentiment dictionary is : ", sentiment_dict)
    print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
    print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
    print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")
    print("Sentence Overall Rated As", end = " ")
    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        print("Positive")
    elif sentiment_dict['compound'] <= - 0.05 :
        print("Negative")
    else :
        print("Neutral")
    sentiment_df     = pd.DataFrame.from_dict(sentiment_dict,orient = 'index')
    return sentiment_dict,sentiment_df
        
title_sentiment_dict = dict()
i = 0
for title in reddit_df['title']:
    tokenized_title    = sent_tokenize(title)
    title_filtered = [x for x in tokenized_title  if x not in a]
    sentiment_dict,sentiment_df  = sentiment_scores(title_filtered)
    title_sentiment_dict[i]   = sentiment_df 
    i    = i+1
    
    
sentiment_analyzer_result = pd.concat(title_sentiment_dict,axis =1).transpose()
new_df     = pd.DataFrame(index = sentiment_analyzer_result.index, columns = ['neg', 'neu', 'pos', 'compound', 'label'])

for i in  range(len(sentiment_analyzer_result)):
    row      = sentiment_analyzer_result.iloc[i,:]
    if row['compound'] >= 0.05 :
        row['label'] = "Positive"
    elif row['compound'] <= - 0.05 :
        row['label']  = "Negative"
    else :
        row['label']  = "Neutral"
    new_df .iloc[i,:]  = row
new_df.to_csv('sentiment_analyzer_result.csv')
new_df  = new_df.reset_index()
new_df  = new_df.drop(columns = ['level_1'])
new_df   = new_df.set_index('level_0')
pd.concat([reddit_df,new_df],axis =1).to_csv('text_and_label.csv')

body_sentiment_dict = dict()
i = 0
for body_main in reddit_df['body']:
    if math.isnan(body_main):
        body_sentiment_dict[i] = np.nan
    
    else:
        tokenized_body    = sent_tokenize(body_main)
        body_filtered = [x for x in tokenized_body  if x not in a]
        sentiment_dict_body,sentiment_df_body  = sentiment_scores(body_filtered)
        body_sentiment_dict[i]   = sentiment_df_body 
    i    = i+1
    
