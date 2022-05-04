#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 20:55:06 2022

@author: laixu
"""

# Data Investigation
import os
import pandas as pd
import numpy as np
import itertools
from matplotlib import pyplot as plt
os.chdir('/Users/laixu/Documents/Machine learning CS 229/project/wsb-stock-prediction/')
data_path  = './dataset/'
reddit_df = pd.read_csv(data_path + 'reddit_wsb.csv')


def daily_reddit_df(reddit_df):
    reddit_df['post_amout'] = 1
    reddit_df['timestamp'] = pd.to_datetime(reddit_df['timestamp'])
    reddit_df_d = reddit_df.groupby(reddit_df['timestamp'].dt.floor('d')).size().reset_index(name='count')

    reddit_df_d = reddit_df_d.set_index('timestamp')
    return reddit_df_d

reddit_df_d = daily_reddit_df(reddit_df)
def post_time_plot(reddit_df_d):

    plt.figure()
    plt.scatter(reddit_df_d.index,reddit_df_d['count'])
    plt.xticks(rotation = 90)
    plt.title('Number of post by day')
    reddit_df_d.plot()
    
def post_time_plot_day(reddit_df_d):
    outlier_date   = reddit_df_d.index.min()
    dates_filtered   = reddit_df_d.index.delete(0)
    reddit_df_d      = reddit_df_d.loc[dates_filtered]
    reddit_df_d
    plt.subplot(3,3,1)
        