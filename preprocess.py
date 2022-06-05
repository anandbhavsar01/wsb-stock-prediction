import regex

def get_words(post):
    split_l = post.split(" ")
    tmp_list = ' '.join(split_l).split()
    normd = [ww.lower() for ww in tmp_list]
    return normd

def remove_links(post):
    url_pattern = regex.compile(r'https?//\S+|www\.\S+')
    return url_pattern.sub(r'', post)
    
def remove_bad_chars(post):
    #print(post)
    other_chars = ['*', '[', ']', '; ',":","“","“","”","-","=","|","^"] 
    for char in other_chars:
        post = post.replace(char, '')
    return post

def get_processed_data(data):
    data=data.reset_index()
    
    # remove bad characters
    data["title"]=data["title"].apply(remove_bad_chars)
    
    # remove all links present in a post title
    data["title"]=data["title"].apply(remove_links)
    
    # put posts into list of words
    data["title"]=data["title"].apply(get_words)
    return data

def convert_to_dict(data,col):
    my_dict = {}
    for index, row in data.iterrows():
        my_dict[index] = row[col]
    return my_dict


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

import numpy as np

def convert_to_matrix(dataset):
    words = {}
    count = 1
    for i in range(0,len(dataset)):
        for word in dataset[i].values():
            if not words.get(word):
                words[word] = count
                count += 1
    dataset_mat = np.zeros((len(dataset),count))
    for i in range(0,len(dataset)):
        for word in dataset[i].values():
            dataset_mat[i][words[word]] += 1
    return dataset_mat