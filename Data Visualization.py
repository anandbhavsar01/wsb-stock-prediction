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
    month_end_dates  = ['2021-01-28','2021-02-28','2021-03-29','2021-04-30','2021-05-31',
                        '2021-06-30','2021-07-31','2021-08-31']
    
    splitted_df_list   = []
    for i in range(len(month_end_dates)-1):
        tmp            = reddit_df_d.loc[month_end_dates[i]:month_end_dates[i+1]]
        splitted_df_list.append(tmp)
    
    fig,axs   = plt.subplot(3,3,1)
    axs = axes.ravel()
    i = 1
    for df in splitted_df_list:
        axs[i].plot(splitted_df_list.index, splitted_df_list)
        plt.yscale('log')
            