import numpy as np
import emoji
import regex



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

f = open('dataset/reddit_wsb.csv', "r")
mat = extract_emojis(f)
for emoji_val in mat.keys():
    print(emoji_val, np.sum(mat[emoji_val]))