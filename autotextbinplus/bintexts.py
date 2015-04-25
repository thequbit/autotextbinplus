#
# Auto Text Bin Plus
#

import numpy as np

import nltk
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.naive_bayes import MultinomialNB

import glob

def clean_text(text, language='english'):

    # only return upper and lower-case letters, and 
    # make text blog lowercase
    text = re.sub('[^a-zA-Z]',' ',text).lower()

    # get all of the words from the text blog
    words = text.split()

    # remove stop words
    stopwords = set(nltk.corpus.stopwords.words(language))
    useful_words = [w for w in words if not w in stopwords]

    # re-generate the 'clean' text blob
    cleaned_text = ' '.join(useful_words)

    return cleaned_text

def build_bag_of_words(ctexts): #, build_dist=False):

    print type(ctexts)

    count_vect = CountVectorizer()
    counts = count_vect.fit_transform(ctexts)

    #tfidf_vect = TfidfVectorizer()
    #features = tfidf_vect.fit_transform(ctexts) #.toarray()

    tfidf_trans = TfidfTransformer()
    features = tfidf_trans.fit_transform(counts)

    #dist = None
    #if build_dist == True:
    #   dist = []
    #   _d = np.sum(data_features.toarray(), axis=0)
    #   vocab = vectorizer.get_feature_names()
    #   for tag, count in zip(vocab, _d):
    #       dist.append((count, tag))
   
    return count_vect, tfidf_trans, counts, features

def calculate_vector(texts):
    
    ctexts = []
    #raw_word_count = 0
    #clean_word_count = 0
    for text in texts:
        ctext = clean_text(text)
        ctexts.append(ctext)
        #raw_word_count += len(text.split())
        #clean_word_count += len(ctext.split())
    count_vect, tfidf_trans, counts, features = build_bag_of_words(ctexts) #, build_dist=True)

    return count_vect, tfidf_trans, counts, features, ctexts

def train_classifier(counts, features, ctexts, categories):

    classifier = MultinomialNB().fit(features, categories)

    return classifier

def predict(count_vect, tfidf_trans, classifier, text):

    ctexts = [clean_text(text)]

    #print type(ctexts)

    #count_vect = CountVectorizer()
    counts = count_vect.transform(ctexts)
    
    #fidf_vect = TfidfVectorizer(min_df=1)
    features = tfidf_trans.fit_transform(counts) #.toarray()

    predicted = classifier.predict(features)

    return predicted

if __name__ == '__main__':

    # get doc files
    doc_files = glob.glob('./data/*.txt')

    #
    # define our prefixes for our different doc categories
    #                0    1     2     3
    #
    doc_prefixes = ['tb','pb', 'ps', 'hp']

    texts = []
    categories = []
    for doc_file in doc_files:
        with open(doc_file,'r') as f:
            for cat in doc_prefixes:
                if cat in doc_file:
                    print 'file: {0}, cat: {1}, index: {2}'.format(doc_file, cat, doc_prefixes.index(cat))
                    texts.append(f.read()[:1024])
                    categories.append(doc_prefixes.index(cat))
                    break

    # perform TF-IDF vectorize on each category
    count_vect, tfidf_trans, counts, features, ctexts = calculate_vector(texts)

    # train based on vectors and categories
    classifier = train_classifier(counts, features, ctexts, categories)

    correct_count = 0
    for doc_file in doc_files:
        with open('./data/ps-doc-2.txt') as f:
            for cat in doc_prefixes:
                if cat in doc_file:
                    text = f.read()[:1024]
                    cat_val = doc_prefixes.index(cat)
     
                    # perform prediction
                    predicted = predict(count_vect, tfidf_trans, classifier, text)

                    correct = False
                    if predicted[0] == cat_val:
                        correct_count += 1
                        correct = True

                    print "file: {0}, cat: {1}, index: {2}, predicted: {3}, correct: {4}".format(doc_file, cat, cat_val, predicted, correct)

                    break

    print "{0}/{1} Correct.".format(correct_count, len(doc_files))

    print 'done'

