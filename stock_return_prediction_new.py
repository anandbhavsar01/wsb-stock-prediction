#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 18:06:19 2022

@author: laixu
"""
!pip install tensorflow==1.15.0 stable-baselines gym-anytrading gym
import os
os.chdir('/Users/laixu/Documents/Machine learning CS 229/Project/wsb-stock-prediction')
#os.chdir('C:/Users/anand/Documents/CS229/project/wsb-stock-prediction')

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
all_ret     = (close_price - close_price.shift(1))/close_price.shift(1)

all_ret.to_csv('./Dataset/close2close_ret.csv')
day_ret.to_csv('./Dataset/open2close_ret.csv')
overnight_ret.to_csv('./Dataset/close2open_ret.csv')

tickers_list    = close_price.columns.tolist()

daily_return_close2close       = close_price.diff(1)/close_price
def get_cumulative_return_plot(df):
    plt.figure(figsize = (15,15))
    for ticker in df.columns:
       ((1+ df[ticker].fillna(0)).cumprod()-1).plot(label = ticker)
    plt.legend(loc = 'lower center',ncol=round(len(df.columns)/4))
get_cumulative_return_plot(daily_return_close2close)


((1+ day_ret).cumprod()-1).sum(axis =1).plot()

def get_portfolio_bench_returns(tickers,return_type, day_ret, overnight_ret, all_ret):
    if (return_type) =='Day':
        df           = day_ret[tickers]
    if (return_type) =='Overnight':
        df           = overnight_ret[tickers]
    if (return_type) =='all':
        df           = all_ret[tickers]
    port_ret         = (1+ df.fillna(0)).cumprod() -1    
    return port_ret

    
def get_corr_dict(sentiment,ret):
    corr_dict    = dict()
    for ticker in ret.columns:
       combined_df     = pd.concat([pd.to_numeric(ret[ticker]),sentiment[ticker].fillna(0)],axis =1)
       combined_df.columns = ['overnight_ret','sentiment_sum']
       combined_df       = combined_df.dropna(how ='any')
       corr_dict[ticker]          = combined_df.corr().values[0,1]
    
    return corr_dict 
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


expanding_mean             = sorted_sentiment_daily_sum.expanding(1).mean()
expanding_std              = sorted_sentiment_daily_sum.expanding(1).std()
expanding_z                = expanding_mean/expanding_std
expanding_z.to_csv('./Dataset/sentiment_by_ticker_tszscore.csv')
# use the average first, generate correlation

corr_dict_mean = dict()
for ticker in sorted_sentiment_daily_mean.columns:
    combined_df     = pd.concat([pd.to_numeric(overnight_ret[ticker]),sorted_sentiment_daily_mean[ticker].fillna(0)],axis =1)
    combined_df.columns = ['overnight_ret','sentiment_mean']
    combined_df       = combined_df.dropna(how ='any')
    overnight_ret_ticker     = combined_df[['overnight_ret']]
    sentiment_mean_ticker    = combined_df[['sentiment_mean']]
    corr_dict_mean[ticker]          = combined_df.corr().values[0,1]
    
    
corr_dict_sum = dict()
for ticker in sorted_sentiment_daily_mean.columns:
    combined_df     = pd.concat([pd.to_numeric(overnight_ret[ticker]),sorted_sentiment_daily_sum[ticker].fillna(0)],axis =1)
    combined_df.columns = ['overnight_ret','sentiment_sum']
    combined_df       = combined_df.dropna(how ='any')
    corr_dict_sum[ticker]          = combined_df.corr().values[0,1]

corr_sum_df       = pd.DataFrame(corr_dict_sum, index = ['Correlation']).T
corr_sum_df_abs   = np.abs(corr_sum_df)
corr_sum_df_abs   = corr_sum_df_abs.sort_values('Correlation',ascending=False)
tmp               = pd.concat([corr_sum_df_abs,corr_sum_df ],axis =1)
tmp.columns       = ['Abs_correlation','Correlation']

tickers          = sorted_sentiment_daily_mean.columns

port_ret         = get_portfolio_bench_returns(tickers,'all', day_ret, overnight_ret, all_ret)
port_ret.sum(axis =1).plot()

port_ret_day         = get_portfolio_bench_returns(tickers,'Day', day_ret, overnight_ret, all_ret)
port_ret_day.sum(axis =1).plot()
port_ret_day.plot()

port_ret_night         = get_portfolio_bench_returns(tickers,'Overnight', day_ret, overnight_ret, all_ret)
port_ret_night.sum(axis =1).plot()
port_ret_night.plot()


def trade_based_on_sentiment(ret, sentiment):
    trade_choice      = (sentiment.shift(1))
    port_ret          = (1+ (trade_choice * ret).fillna(0)).cumprod() -1
    port_ret          = port_ret.sum(axis =1)
    return port_ret

selected_tickers      = ['PLTR','GME','BY','BB','SNDL','AMC','SPCE']
port_ret_all  = trade_based_on_sentiment(day_ret[selected_tickers],expanding_z)





# time series z score sentiment sum

# time series z score sentiment mean

# we use purchasing 1 share for all the tickers in the portfolio as a 'Buy and hold strategy' for the benchmark comparison purpose.


def get_accuracy_ratio:
    
    
    
    
# compute hit ratio
def get_hit_ratio(sentiment, label):
    accuracy = 0
    points = 0
    for index, row in label.iterrows():
        print(index)
        print(sentiment[str(index)])
        print(row)


# get labeled data
labeled_sentiment = pd.read_excel('dataset/reddit_wsb_final.xlsx').set_index('timestamp')
found_sentiment = pd.read_csv('text_and_label.csv').set_index('timestamp')
print(get_hit_ratio(found_sentiment, labeled_sentiment))
>>>>>>> 732abcc70c0dad7fce02eec5892ef896058fe3e2
