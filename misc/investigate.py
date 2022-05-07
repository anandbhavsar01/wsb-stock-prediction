from re import A
from pandas import DataFrame, read_csv, read_excel
import pandas as pd
import sys
import matplotlib.pyplot as plt
from collections import Counter

file = read_csv(r'../dataset/reddit_wsb.csv')
tickers = read_excel(r'../dataset/tickers.xlsx')
tickers_found = read_csv(r'../dataset/ticker_location.csv')

sorted_comments = file.sort_values(['score'], ascending=False)
print(sorted_comments.head(1))

file.plot(x ='timestamp', y = 'score', rot=45)
plt.tight_layout()
plt.savefig('score_over_time.png')
file.plot(x='timestamp',y='comms_num', rot=45)
plt.tight_layout()
plt.savefig('comments_over_time.png')
file.plot(kind='scatter', x='score', y='comms_num')
plt.savefig('score_to_comments.png')

c = Counter(" ".join(file["title"]).split()).most_common(100)
c = Counter(" ".join(file["title"]).lower().split()).most_common(100)
print(c)

print(file['score'].mean())
print(file['comms_num'].mean())

# Now we want info about the posts that mention a Ticker
file = pd.concat([file, tickers_found['Ticker']], axis=1)
file['isBodyNan'] = file["body"].isnull()

condensed_file = file.dropna(subset=['Ticker'])

condensed_file.plot(x = 'timestamp', y = 'score', rot=45)
plt.tight_layout()
plt.savefig('score_over_time_tick.png')
condensed_file.plot(x='timestamp',y='comms_num', rot=45)
plt.tight_layout()
plt.savefig('comments_over_time_tick.png')
condensed_file.plot(kind='scatter', x='score', y='comms_num')
plt.savefig('score_to_comments_tick.png')

sorted_condensed = condensed_file.sort_values(['score'], ascending=False)
print(sorted_condensed.head(1))

only_text = condensed_file.dropna(subset=['body'])
only_text.plot(x = 'timestamp', y = 'score', rot=45)
plt.tight_layout()
plt.savefig('score_over_time_text.png')
only_text.plot(x='timestamp',y='comms_num', rot=45)
plt.tight_layout()
plt.savefig('comments_over_time_text.png')
only_text.plot(kind='scatter', x='score', y='comms_num')
plt.savefig('score_to_comments_text.png')

sorted_text = only_text.sort_values(['score'], ascending=False)
print(sorted_text.head(1))