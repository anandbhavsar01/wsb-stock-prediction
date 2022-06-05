import preprocess
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
# Get data
print('Opening Data')
data = pd.read_csv('dataset/reddit_wsb_returns_final.csv')

# Preprocess
print('Preprocessing')
processed = preprocess.get_processed_data(data)
dict_titles = preprocess.convert_to_dict(processed,"title")
filtered_titles = preprocess.remove_stop_words(dict_titles)

dataset = []
for i in filtered_titles.keys():
    sentence = filtered_titles[i]
    dict_sentence = {}
    for j in range(0,len(sentence)):
        dict_sentence[j] = sentence[j]
    dataset.append(dict_sentence)

dataset_mat = preprocess.convert_to_matrix(dataset)

print('Preprocessing Complete')

X_train = dataset_mat[:int(len(dataset_mat)*0.8)]
X_test = dataset_mat[int(len(dataset_mat)*0.8):]
y_train = data['Sign'][:int(len(dataset_mat)*0.8)]
y_test = data['Sign'][int(len(dataset_mat)*0.8):]
#X_train, X_test, y_train, y_test = train_test_split(dataset_mat, data['return'], test_size=0.2)

clf = GaussianNB()
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
y_valid = clf.predict(X_train)

from sklearn import metrics
print("Accuracy", metrics.accuracy_score(y_test,y_pred))
print("Accuracy", metrics.accuracy_score(y_train,y_valid))



data = pd.read_csv('dataset/text_and_label.csv')

# Preprocess
print('Preprocessing')
processed = preprocess.get_processed_data(data)
dict_titles = preprocess.convert_to_dict(processed,"title")
filtered_titles = preprocess.remove_stop_words(dict_titles)

dataset = []
for i in filtered_titles.keys():
    sentence = filtered_titles[i]
    dict_sentence = {}
    for j in range(0,len(sentence)):
        dict_sentence[j] = sentence[j]
    dataset.append(dict_sentence)

dataset_mat = preprocess.convert_to_matrix(dataset)

sentiment_mapper = {'Negative':-1,
                    'Neutral':0,
                    'Positive':1}

data['score'] = data['label'].map(sentiment_mapper)

X = dataset_mat
y = data['score']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

clf = GaussianNB()
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
y_valid = clf.predict(X_train)

from sklearn import metrics
print("Accuracy", metrics.accuracy_score(y_test,y_pred))
print("Accuracy", metrics.accuracy_score(y_train,y_valid))
