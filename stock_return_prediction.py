#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:06:19 2022

@author: laixu
"""
import os
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
#.columns[0] = ['DATE']
close_price  = close_price.set_index('index')

daily_return_close2close       = close_price.diff(1)/close_price
def get_cumulative_return_plot(df):
    plt.figure(figsize = (15,15))
    for ticker in df.columns:
       ((1+ df[ticker].fillna(0)).cumprod()-1).plot(label = ticker)
    plt.legend(loc = 'lower center',ncol=round(len(df.columns)/4))
get_cumulative_return_plot(daily_return_close2close)


# get the sentiment by ticker
VADER_sentiment = pd.read_csv('text_and_label.csv')
ticker_location         = pd.read_csv('./dataset/' + 'ticker_location.csv')
ticker_list             = pd.read_csv('')
def_get_sentiment_by_ticker(sentiment_label, ticker_location):
    ticker_sentiment_df     = pd.DataFrame(index = sentiment_label.index, columns = ticker_list)
    