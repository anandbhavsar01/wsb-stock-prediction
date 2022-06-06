import preprocess
import pandas as pd
import nltk

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
    dataset.append( (dict_sentence, data['Sign'][i] ) )
print('Preprocessing Complete')

# Create train and test set
train = dataset[:int(len(dataset)*0.8)]
test = dataset[int(len(dataset)*0.8):]

print('Running Decision Tree')
classifier = nltk.classify.DecisionTreeClassifier.train(train, entropy_cutoff=0, support_cutoff=0)
sorted(classifier.labels())
print('Decision Tree Accuracy', nltk.classify.accuracy(classifier, test))


max_depth_list = [100, 200, 300, 400, 500, 600, 700, 800]

from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

clf = DecisionTreeClassifier()
clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)


accuracy_list = []
for depth in max_depth_list:
    clf = DecisionTreeClassifier(max_depth = depth)
    clf.fit(X_train,y_train)
    y_pred = clf.predict(X_test)
    accuracy = metrics.accuracy_score(y_test,y_pred)
    
    print("Accuracy", metrics.accuracy_score(y_test,y_pred))