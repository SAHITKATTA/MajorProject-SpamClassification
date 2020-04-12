import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
data = {'message': "test"}
loaded_model = pickle.load(open('./model/spam_classifier.sav', 'rb'))
loaded_vectorizer = pickle.load(open("./model/tfidfvectorizer.pickle", "rb"))
spam_dict = {1: "SPAM", 0: "NOT SPAM"}
list_of_new_testing_data = []
list_of_new_testing_data.append(data['message'])
print(data['message'])
tranformed_data = loaded_vectorizer.transform(list_of_new_testing_data)
predictions = loaded_model.predict(tranformed_data)
print(spam_dict[predictions[0]])
