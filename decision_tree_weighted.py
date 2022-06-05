import preprocess
import pandas as pd
import nltk

def run_model(sign):
    # Get data
    print('Opening Data')
    #data = pd.read_csv('dataset/reddit_wsb_returns_final.csv')
    data = pd.read_csv('dataset/reddit_wsb_comms_score_weighted.csv')

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
        dataset.append( (dict_sentence, data[sign][i] ) )
    print('Preprocessing Complete')

    # Create train and test set
    import random
    #random.shuffle(dataset)
    train = dataset[:int(len(dataset)*0.8)]
    test = dataset[int(len(dataset)*0.8):]

    print('Running Decision Tree')
    classifier = nltk.classify.DecisionTreeClassifier.train(train, entropy_cutoff=0, support_cutoff=0)
    sorted(classifier.labels())
    print('Decision Tree Num Comments Train Accuracy', nltk.classify.accuracy(classifier, train))
    print('Decision Tree Num Comments Test Accuracy', nltk.classify.accuracy(classifier, test))

    predictions = []
    for i in range(0,len(dataset)):
        predictions.append([dataset[i][0],classifier.classify(dataset[i][0])])
    predictions_df = pd.DataFrame(predictions, columns=['text','prediction'])
    predictions_df.to_csv('dataset/decision_tree'+sign+'.csv')

run_model('comm_sign')
run_model('score_sign')

