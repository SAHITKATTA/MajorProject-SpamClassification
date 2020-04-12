# ref: https://www.independent.co.uk/life-style/history/42-the-answer-to-life-the-universe-and-everything-2205734.html
# ref: https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472
# ref: https://www.kaggle.com/uciml/sms-spam-collection-dataset - UCI MACHINE LEARNING
# Importing Libraries
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
import pickle
from sklearn import metrics
# Importing The Data-set
data = pd.read_csv("./input/Dataset.csv")

# Text Pre-processing
texts = []
labels = []
for i, label in enumerate(data['Category']):
    texts.append(data['Message'][i])
    if label == 'legit':
        labels.append(0)
    else:
        labels.append(1)

X = np.asarray(texts)
y = np.asarray(labels)
print("number of texts :" , len(texts))
print("number of labels: ", len(labels))

# Converting Text to Numbers (TfidfVectorizer process)
vectorizer = TfidfVectorizer()
vectorized_text = vectorizer.fit_transform(X)

# Training and Test Sets
X_train, X_test, y_train, y_test = train_test_split(vectorized_text, y, random_state=42)
print("X_train: {}, X_test: {}, y_train: {}, y_test: {}".format(X_train.shape, X_test.shape, y_train.shape, y_test.shape))
# Training Text Classification Model
spam_classifier = LinearSVC()
spam_classifier = spam_classifier.fit(X_train,y_train)

# Evaluating The Model
y_pred = spam_classifier.predict(X_test)
    # Model Accuracy: how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

    # Model Precision: what percentage of positive tuples are labeled as such?
print("Precision:",metrics.precision_score(y_test, y_pred))

    # Model Recall: what percentage of positive tuples are labelled as such?
print("Recall:",metrics.recall_score(y_test, y_pred))
print(spam_classifier.score(X_test,y_test))

# Saving and Loading the Model
    # Saving
filepath = './model/spam_classifier.sav'
pickle.dump(spam_classifier, open(filepath, 'wb'))
pickle.dump(vectorizer, open("./model/tfidfvectorizer.pickle", "wb"))

    #Loading
loaded_model = pickle.load(open(filepath, 'rb'))
result = loaded_model.score(X_test, y_test)
print(result)
# Prediction
spam_dict = {1: "SPAM", 0: "NOT SPAM"}
list_of_new_testing_data = ["free prizes congratulations you have won iPhone text to 2342342","Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121"]
tranformed_data = vectorizer.transform(list_of_new_testing_data)
predictions = loaded_model.predict(tranformed_data)
for text, prediction in zip(list_of_new_testing_data,predictions):
    print("For given text:\n\t\""+text+"\" IS "+""+ spam_dict[prediction])
