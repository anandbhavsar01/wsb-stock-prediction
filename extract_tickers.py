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
    
def cross_check_txt_ticker(tickers, split_text_dict):
    txt_list                = []
    txt_ticker              = dict()
    for key in split_text_dict.keys():
        txt_ticker[key]      = [set(tickers) & set(split_text_dict[key])]
        if len(txt_ticker[key])!=0:
            txt_list.append(txt_ticker[key])
    ticker_counter = {item:txt_list.count(item) for item in txt_list}
    ticker_counter = {k: v for k, v in sorted(ticker_counter.items(),reverse = True, key=lambda x: x[1])}
    ticker_counter_top10 = ticker_counter[:10]
    
    for key in split_text_dict.keys():
        txt_ticker[key]      = [set(ticker_counter_top10.keys()) & set(split_text_dict[key])]
        if len(txt_ticker[key])!=0:
            txt_list.append(txt_ticker[key])
            
    return txt_ticker

reddit_dict  = make_dict_title(reddit_df)
split_text_dict  = get_split_text_from_dict(reddit_dict)
tmp = cross_check_txt_ticker(tickers, split_text_dict)

# count all the tickers 
