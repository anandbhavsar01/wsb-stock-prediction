#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 14:51:44 2022

@author: laixu
"""
#import yfinance
#yfinance.Tickers()
import os
import pandas as pd
import numpy as np
import itertools
os.chdir('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/')
data_path  = './dataset/'
reddit_df = pd.read_csv(data_path + 'reddit_wsb.csv')
equity_tickers   = pd.read_excel(data_path + 'tickers.xlsx', sheet_name = 'stocks',index_col = None)['Symbol']
crypto_tickers   = pd.read_excel(data_path + 'tickers.xlsx', sheet_name = 'crypto', index_col = None)['Symbol']
tickers          = np.append(equity_tickers,crypto_tickers).tolist()
tickers_list     = []
for ticker in tickers:
  #  print(ticker)
    tickers_list.append(ticker.lower())
    
    
def make_dict_title(reddit_df):
    post_dict   = dict()
    for i in range(len(reddit_df)):
        ID          = reddit_df.index[i]
        post_dict[ID]  = reddit_df.iloc[i]['title']
    return post_dict

def make_dict_body(reddit_df):
    post_dict_body  = dict()
    for i in range(len(reddit_df)):
        ID          = reddit_df.index[i]
        post_dict_body[ID]  = reddit_df.iloc[i]['body']
    return post_dict_body

def get_words(post):
    split = post.split(' ')
    normd  = split
    #normd = [ww.lower() for ww in split]
    return normd

def get_split_text_from_dict(post_dict):
    split_text_dict = dict()
    for key in post_dict.keys():
        normd  = get_words(post_dict[key])
        split_text_dict[key] = normd
    return split_text_dict

def distinct_item_counter_from_list(word_list):
    txt_counter       = dict()
    for word in itertools.chain(*word_list):
      #  print(word)
        if word in list(txt_counter.keys()):
            txt_counter[word]  = txt_counter[word] + 1
              
        else:
            txt_counter[word]  = 1 
    return txt_counter
    
def cross_check_txt_ticker(tickers, split_text_dict):
    txt_list                = []
    txt_ticker              = dict()
    txt_ticker_location     = dict()
    for key in split_text_dict.keys():
        txt_ticker[key]      = set(tickers).intersection(set(split_text_dict[key]))
        if len(txt_ticker[key])!= 0:
            txt_list.append(txt_ticker[key])
    ticker_counter = distinct_item_counter_from_list(txt_list)
    # convert dictionary to df and sort
    ticker_counter_df = pd.DataFrame.from_dict(ticker_counter,orient = 'index')
    ticker_counter_df.columns = ['count']
    ticker_counter_df = ticker_counter_df.sort_values(by = 'count',ascending = False).iloc[:50]
    # more rigid method is to cross cehck data base of top most commonly used american words but 
    # due to time constraint, in our existing analysis we are just manually knock out words that are
    # not tickers.
    # note that the knockout_words should follow your ticker counter df
    knockout_words   = ['A','IS','YOU','ON','FOR','ARE','DO','GO','UP','NOW','BE','GET','ALL','IT',
                        'CAN','WE','BE','REAL','ME','LOVE','HAS','NEXT','OR','NEW','OUT','REAL','SO','BIG','UK']
    
    txt_ticker_list  = set(ticker_counter_df.index) ^ set(knockout_words)
    for key in split_text_dict.keys():
        txt_ticker[key]      = [set(split_text_dict[key]) & set(tickers)]
        
    for key in split_text_dict.keys():
        txt_ticker_location[key]      = [set(split_text_dict[key]) & set(txt_ticker_list)]
            
    
    return txt_ticker_list,txt_ticker_location

reddit_dict  = make_dict_title(reddit_df)
split_text_dict  = get_split_text_from_dict(reddit_dict)
txt_ticker,txt_ticker_location= cross_check_txt_ticker(tickers, split_text_dict)

txt_ticker_location_df = pd.DataFrame.from_dict(txt_ticker_location, orient = 'index')
txt_ticker_location_df.to_csv('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/ticker_location.csv')
# count all the tickers 
