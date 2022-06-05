import preprocess
import pandas as pd

# Get data
print('Opening Data')
data = pd.read_csv('dataset/reddit_wsb.csv')

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
df = pd.DataFrame(dataset_mat, columns=[''])
df.to_csv(index=False)

print(dataset_mat)