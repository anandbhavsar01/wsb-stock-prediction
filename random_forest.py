import preprocess
import pandas as pd
from sklearn.model_selection import train_test_split

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

from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)

from sklearn import metrics
print("Accuracy", metrics.accuracy_score(y_test,y_pred))