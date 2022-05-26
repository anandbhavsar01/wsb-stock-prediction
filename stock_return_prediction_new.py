#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:06:19 2022

@author: laixu
"""

import os
os.chdir('/Users/laixu/Documents/Machine learning CS 229/Project/wsb-stock-prediction')
import pandas as pd
import numpy as np
import itertools
from matplotlib import pyplot as plt
from datetime import datetime
# stock return analysis
stock_price = pd.read_excel('tickerdata.xlsx',sheet_name= 'Sheet1',index_col=[0])
stock_tickers = stock_price.filter(regex='^(?!Unnamed)').columns
new_col       = np.repeat(stock_tickers,5)
stock_price.columns = new_col
close_price         = stock_price.loc[:,stock_price.iloc[0,]=='Close']
open_price          = stock_price.loc[:,stock_price.iloc[0,]=='Open']
volume             = stock_price.loc[:,stock_price.iloc[0,]=='Volume']

close_price        = close_price.reset_index()
close_price        = close_price .drop(index = [0,1])
close_price  = close_price.set_index('index')

#.columns[0] = ['DATE']

open_price        = open_price.reset_index()
open_price        = open_price .drop(index = [0,1])
open_price  = open_price.set_index('index')
#.columns[0] = ['DATE']


overnight_ret    = (open_price - close_price.shift(1))/close_price.shift(1)
day_ret    = (close_price - open_price)/open_price

tickers_list    = close_price.columns.tolist()

daily_return_close2close       = close_price.diff(1)/close_price
def get_cumulative_return_plot(df):
    plt.figure(figsize = (15,15))
    for ticker in df.columns:
       ((1+ df[ticker].fillna(0)).cumprod()-1).plot(label = ticker)
    plt.legend(loc = 'lower center',ncol=round(len(df.columns)/4))
get_cumulative_return_plot(daily_return_close2close)


# get the sentiment by ticker
VADER_sentiment = pd.read_csv('text_and_label.csv').set_index('timestamp')
ticker_location         = pd.read_csv('./dataset/' + 'ticker_location.csv')
ticker_location         = ticker_location.dropna(how = 'any')
ticker_location      = ticker_location.apply(lambda x:x.Ticker.replace("{'",'').replace("'}",'').replace("', '",' '),axis =1)

# mapping sentiment to ticker
sentiment_df        = pd.DataFrame(index = VADER_sentiment.index ,columns = tickers_list)
for i in range(len(ticker_location)):
    ticker_list  = ticker_location.iloc[i].split(' ')
    for ticker in ticker_list:
        post_num     = ticker_location.index[i]
        sentiment_df.iloc[post_num][ticker]   = VADER_sentiment.iloc[post_num]['label']
            
sentiment_df.to_csv('./Dataset/sentiment_by_ticker.csv')
sentiment_df_filled    = sentiment_df.fillna(method = 'ffill')
sentiment_df_filled.to_csv('./Dataset/sentiment_by_ticker_filleddown.csv')

sentiment_df_sorted = sentiment_df_filled.sort_index()
sentiment_df_sorted.iloc[1:,].to_csv('./Dataset/sentiment_by_ticker_filledsorted.csv')

sorted_sentiment  = pd.read_csv('./Dataset/sentiment_by_ticker_filledsorted.csv').set_index('timestamp')
sorted_sentiment.index = pd.to_datetime(sorted_sentiment.index)

sorted_sentiment    = sorted_sentiment.replace({'Positive':1,
                                                'Neutral':0,
                                                'Negative':-1})

# aggregate sentiment by day
sorted_sentiment['Day']    = sorted_sentiment.index.floor('D')
sorted_sentiment_daily_sum     = sorted_sentiment.groupby('Day').sum()
sorted_sentiment_daily_sum.to_csv('./Dataset/sentiment_by_ticker_sum.csv')
sorted_sentiment_daily_mean     =  sorted_sentiment.groupby('Day').mean()
sorted_sentiment_daily_mean.to_csv('./Dataset/sentiment_by_ticker_mean.csv')

# use the average first, generate correlation
corr_dict_mean = dict()
for ticker in corr_df.columns:
    combined_df     = pd.concat([pd.to_numeric(overnight_ret[ticker]),sorted_sentiment_daily_mean[ticker].fillna(0)],axis =1)
    combined_df.columns = ['overnight_ret','sentiment_mean']
    combined_df       = combined_df.dropna(how ='any')
    overnight_ret_ticker     = combined_df[['overnight_ret']]
    sentiment_mean_ticker    = combined_df[['sentiment_mean']]
    corr_dict_mean[ticker]          = combined_df.corr().values[0,1]
    
    
corr_dict_sum = dict()
for ticker in corr_df.columns:
    combined_df     = pd.concat([pd.to_numeric(overnight_ret[ticker]),sorted_sentiment_daily_sum[ticker].fillna(0)],axis =1)
    combined_df.columns = ['overnight_ret','sentiment_sum']
    combined_df       = combined_df.dropna(how ='any')
    overnight_ret_ticker     = combined_df[['overnight_ret']]
    sentiment_mean_ticker    = combined_df[['sentiment_sum']]
    corr_dict_sum[ticker]          = combined_df.corr().values[0,1]
    
# time series z score sentiment sum

# time series z score sentiment mean
    
def get_corr_dict(sentiment,ret):
    corr_dict    = dict()
    for ticker in ret.columns:
       combined_df     = pd.concat([pd.to_numeric(ret[ticker]),sentiment[ticker].fillna(0)],axis =1)
       combined_df.columns = ['overnight_ret','sentiment_sum']
       combined_df       = combined_df.dropna(how ='any')
       corr_dict[ticker]          = combined_df.corr().values[0,1]
    
    return corr_dict 


# compute hit ratio

