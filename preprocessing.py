import numpy as np
import emoji
import regex



def extract_emojis(input_file):
    emoji_list = []
    emoji_mat = {}
    comments = input_file.readlines()
    for line in comments:
        comment = line[0]
        data = regex.findall(r'\X', comment)
        for word in data:
            if any(char in emoji.EMOJI_DATA for char in word):
                if word not in emoji_list:
                    emoji_list.append(word)
    
    for key in emoji_list:
        emoji_mat[key] = np.zeros(len(comments)-1)

    i = 0
    for line in comments:
        comment = line[0]
        data = regex.findall(r'\X', comment)
        for word in data:
            for char in word:
                if emoji_mat.get(char) is not None:
                    emoji_mat[char][i] += 1
        i += 1
    return emoji_mat

f = open('dataset/reddit_wsb.csv', "r")
print(extract_emojis(f))