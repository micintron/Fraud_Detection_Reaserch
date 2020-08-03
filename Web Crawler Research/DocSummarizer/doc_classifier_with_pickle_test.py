import numpy as np
import pandas as pd
import requests
import pickle
from bs4 import BeautifulSoup
from collections import Counter
import sklearn
from sklearn import linear_model
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import logging

'''
# save 20 newsgroups data to .csv file
def twenty_newsgroup_to_csv():
    newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

    df = pd.DataFrame([newsgroups_train.data, newsgroups_train.target.tolist()]).T
    df.columns = ['text', 'target']

    targets = pd.DataFrame(newsgroups_train.target_names)
    targets.columns = ['title']

    out = pd.merge(df, targets, left_on='target', right_index=True)
    out['date'] = pd.to_datetime('now')
    out.to_csv('20_newsgroup.csv')


twenty_newsgroup_to_csv()
'''

# Load in dataset
data = pd.read_csv('20_newsgroup.csv').dropna()
categories = data['title']
text = data['text']
labels = sorted(list(set(categories)))
print(labels)


def count_data(labels, categories):
    '''
    Create a counter to display how a dataset is split into multiple categories

    :param labels: types of categories
    :param categories: full list of categories given to all texts
    :return: counter created from dataset
    '''
    c = Counter(categories)
    cont = dict(c)
    # total number of news
    tot = sum(list(cont.values()))
    d = {
        "category": labels,
        "count": [cont[l] for l in labels],
        "percent": [cont[l] / tot for l in labels]
    }

    print(pd.DataFrame(d))
    print("total \t", tot)

    return cont


def train_test(iterations: int):
    '''
    create multiple classifier models and save the most accurate ones
    :param iterations: number of models we will create
    '''
    global x_train, x_test, y_train, y_test, text_clf
    # Code adapted from that of Matthew Cintron
    best = 0
    for _ in range(iterations):
        # split data into train and test
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(text, categories, test_size=0.1)
        text_clf = Pipeline([('vect', CountVectorizer()),
                             ('tfidf', TfidfTransformer()),
                             ('clf', MultinomialNB()),
                             ])
        text_clf = text_clf.fit(x_train, y_train)

        accuracy = text_clf.score(x_test, y_test)
        print('the total accuracy of predictions was = ' + str(accuracy))

        # code to save our best models
        if accuracy > best:
            best = accuracy
            with open("20news_model.pickle", "wb") as f:
                pickle.dump(text_clf, f)


x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(text, categories, test_size=0.1)
cont = count_data(labels, categories)
train_test(100)

#load saved model
pickle_in = open("20news_model.pickle", "rb")
text_clf = pickle.load(pickle_in)

# Test model
predicted = text_clf.predict(x_test)

acc = text_clf.score(x_test, y_test)
print("total accuracy was " + str(acc))

