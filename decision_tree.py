import preprocess
import pandas as pd

data = pd.read_csv('dataset/reddit_wsb_returns.csv')
processed = preprocess.get_processed_data(data)
my_dict = preprocess.convert_to_dict(processed,"title")




