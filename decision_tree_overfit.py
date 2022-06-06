#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:12:27 2022

@author: laixu
"""
import numpy as np
import emoji
import regex
import pandas as pd
import nltk
file = pd.read_csv('dataset/text_and_label.csv')
data_and_labels = pd.concat([file['title'], file['label']], axis=1)
import numpy as np
def extract_emojis(input_file):
    emoji_list = []
    emoji_mat = {}
    posts = input_file.readlines()
    for line in posts:
        post = line[0]
        data = regex.findall(r'\X', post)
        for word in data:
            if any(char in emoji.EMOJI_DATA for char in word):
                if word not in emoji_list:
                    emoji_list.append(word)
    
    for key in emoji_list:
        emoji_mat[key] = np.zeros(len(posts)-1)

    i = 0
    for line in posts:
        post = line[0]
        data = regex.findall(r'\X', post)
        for word in data:
            for char in word:
                if emoji_mat.get(char) is not None:
                    emoji_mat[char][i] += 1
        i += 1
    return emoji_mat

def preprocess(f_in):
    print("[preprocess::extract emojis]")
    f = open(f_in, "r")
    my_dict_emoji = extract_emojis(f)

    # open and process
    print("[preprocess::extract titles and body]")
    data = pd.read_csv(f_in)
    processed=get_processed_data(data)
    my_dict_titles = convert_to_dict(processed,"title")
    my_dict_body = convert_to_dict(processed,"body")
    print("[preprocess::complete]")
    return my_dict_emoji, my_dict_titles, my_dict_body
def get_words(post):
    split_l = post.split(" ")
    tmp_list = ' '.join(split_l).split()
    normd = [ww.lower() for ww in tmp_list]
    return normd

def remove_links(post):
    url_pattern = re.compile(r'https?//\S+|www\.\S+')
    return url_pattern.sub(r'', post)
    
def remove_bad_chars(post):
    other_chars = ['*', '[', ']', '; ',":","“","“","”","-","=","|","^"] 
    for char in other_chars:
        post = post.replace(char, '')
    return post
def get_processed_data(data):
    data.dropna(subset=['body'], inplace=True)
    data=data.reset_index()
    
    # remove bad characters
    data["body"]=data["body"].apply(remove_bad_chars)
    data["title"]=data["title"].apply(remove_bad_chars)
    
    # remove all links present in a post title and body
    data["body"]=data["body"].apply(remove_links)
    data["title"]=data["title"].apply(remove_links)
    
    # put posts into list of words
    data["body"]=data["body"].apply(get_words)
    data["title"]=data["title"].apply(get_words)
    return data

def convert_to_dict(data,col):
    my_dict = {}
    for index, row in data.iterrows():
        my_dict[index] = row[col]
    return my_dict
dict_emojis, dict_titles, dict_body = preprocess('dataset/reddit_wsb.csv')
msk = np.random.rand(len(data_and_labels)) < 0.8
train = data_and_labels[msk].to_records(index=False)
for i in range(0,len(train)):
    data = {}
    title = train[i][0].split()
    for j in range(0,len(title)):
        data[j] = title[j]
    train[i] = (data, train[i][1])
test = data_and_labels[~msk].to_records(index=False)
for i in range(0,len(test)):
    data = {}
    title = test[i][0].split()
    for j in range(0,len(title)):
        data[j] = title[j]
    test[i] = (data, test[i][1])
print(train)

dict_emojis, dict_titles, dict_body = preprocess('dataset/reddit_wsb.csv')
#print(dict_emojis, dict_titles, dict_body)
from nltk.corpus import stopwords

def remove_stop_words(dict_sentences):
    stop_words = set(stopwords.words('english'))
    for i in dict_sentences.keys():
        filtered = []
        for word in dict_sentences[i]:
            if word not in stop_words:
                filtered.append(word)
        dict_sentences[i] = filtered
    return dict_sentences

filtered_titles = remove_stop_words(dict_titles)

dataset = []
for i in filtered_titles.keys():
    sentence = filtered_titles[i]
    dict_sentence = {}
    for j in range(0,len(sentence)):
        dict_sentence[j] = sentence[j]
    dataset.append( (dict_sentence, data_and_labels['label'][i] ) )

import random
random.shuffle(dataset)
train = dataset[:int(len(dataset)*0.9)]
test = dataset[int(len(dataset)*0.9):]

classifier = nltk.classify.DecisionTreeClassifier.train(train, entropy_cutoff=0, support_cutoff=0)
sorted(classifier.labels())
#print(classifier)
print(nltk.classify.accuracy(classifier, train))
print(nltk.classify.accuracy(classifier, test))

