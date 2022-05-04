from re import A
from pandas import DataFrame, read_csv
import pandas as pd
import sys
import matplotlib.pyplot as plt
from collections import Counter

file = read_csv(r'../dataset/reddit_wsb.csv')

#sorted_comments = file.sort_values(['score'], ascending=False)
#print(sorted_comments.head(1))

#file.plot(x = 'created', y = 'score')
#plt.savefig('score_over_time.png')
#file.plot(x='created',y='comms_num')
#plt.savefig('comments_over_time.png')
#file.plot(kind='scatter', x='score', y='comms_num')
#plt.savefig('score_to_comments.png')

#c = Counter(" ".join(file["title"]).split()).most_common(100)
#c = Counter(" ".join(file["title"]).lower().split()).most_common(100)
#print(c)

file['isBodyNan'] = file.isNa()

#print(file['score'].mean())
#print(file['comms_num'].mean())