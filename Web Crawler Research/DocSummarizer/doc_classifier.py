import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import logging

# Set up logging config
logging.basicConfig(filename='doc_classifier.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')


def print_menu():
    print("Please Select a Menu Option:")
    print("1. Randomly Select Document to Classify.")
    print("2. Enter your own Document to Classify")
    print("3. Enter URL to Classify")
    print("4. Exit")


def get_article(html: str):
    """
    Retrieves all text with the <p> html tag

    :param html: html page content retrieved from url
    :return: plaintext webpage contents
    """
    soup = BeautifulSoup(html, "html.parser")

    article_text = ''
    article = soup.find_all('p')
    for element in article:
        article_text += '\n' + ''.join(element.findAll(text=True))
    return article_text


# Load the data set - training data.
twenty_train = fetch_20newsgroups(subset='train', shuffle=True)
print("TARGET NAMES: {}".format(twenty_train.target_names))
logging.debug("TARGET NAMES: {}".format(twenty_train.target_names))

text_clf = Pipeline([('vect', CountVectorizer()),    # Extracting features from text files
                     ('tfidf', TfidfTransformer()),  # TF-IDF
                     ('clf', MultinomialNB())])      # Training Naive Bayes (NB) classifier on training data.

text_clf = text_clf.fit(twenty_train.data, twenty_train.target)
logging.debug("Classifier Successfully trained.")

# Performance of NB Classifier
twenty_test = fetch_20newsgroups(subset='test', shuffle=True)
predicted = text_clf.predict(twenty_test.data)
logging.debug("Accuracy Score: {}".format(np.mean(predicted == twenty_test.target)))

menu_choice = "0"

while menu_choice != "4":
    logging.debug("While Loop 1 started...")
    print()
    print_menu()
    menu_choice = input().strip()
    logging.debug("Menu Choice {} Selected...".format(menu_choice))

    if menu_choice == "1":
        # Select random article
        i = np.random.randint(0, len(twenty_test.data))

        logging.debug("Documents in test data: {}".format(len(twenty_test.data)))
        logging.debug("Randomly generated index: {}".format(i))

        print(twenty_test.data[i])
        print("Suggested Category:", twenty_test.target_names[predicted[i]])
        print("Actual Category:", twenty_test.target_names[twenty_test.target[i]])

        logging.debug("Document contents: \n{}".format(twenty_test.data[i]))
        logging.debug("Suggested Category: {}".format(twenty_test.target_names[predicted[i]]))
        logging.debug("Actual Category: ()".format(twenty_test.target_names[twenty_test.target[i]]))

    elif menu_choice == "2":
        # Enter text to classify
        print("Enter text you wish to classify:")
        text_to_predict = input().strip()

        predicted = text_clf.predict([text_to_predict])  # text needs to be an array element
        print("Suggested Category:", twenty_test.target_names[predicted[0]])

        logging.debug("Entered Text: {}".format(text_to_predict))
        logging.debug("Suggested Category: {}".format(twenty_test.target_names[predicted[0]]))

    elif menu_choice == "3":
        # Enter url to classify
        url = input("Enter URL: ").strip()
        logging.debug("Entered URL: {}".format(url))

        # retrieve webpage content
        html = requests.get(url).content
        article = get_article(html)
        logging.debug("Text parsed from URL:\n{}".format(article))

        predicted = text_clf.predict([article])  # article text needs to be an array element
        print("Suggested Category:", twenty_test.target_names[predicted[0]])
        logging.debug("Suggested Category: {}".format(twenty_test.target_names[predicted[0]]))

    logging.debug("End of While Loop 1 Reached")
