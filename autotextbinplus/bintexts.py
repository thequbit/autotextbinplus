#
# Auto Text Bin Plus
#

import numpy as np

import nltk
import re

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

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

def build_bag_of_words(ctexts, build_dist=False):

    # Initalize our TF-IDF vectorizer
    vectorizer = TfidfVectorizer(min_df=1)

    # perform the transform using the TF-IDF values
    data_features = vectorizer.fit_transform(ctexts) #.toarray()

    dist = None
    if build_dist == True:
       dist = []
       _d = np.sum(data_features.toarray(), axis=0)
       vocab = vectorizer.get_feature_names()
       for tag, count in zip(vocab, _d):
           dist.append((count, tag))
    
    return data_features, dist

def calculate_vector(texts):
    
    ctexts = []
    raw_word_count = 0
    clean_word_count = 0
    for text in texts:
        ctext = clean_text(text)
        ctexts.append(ctext)
        raw_word_count += len(text.split())
        clean_word_count += len(ctext.split())
    bow, dist = build_bag_of_words(ctexts, build_dist=True)

    return bow, dist, raw_word_count, clean_word_count

if __name__ == '__main__':

    doc_files = glob.glob('./data/*.txt')

    texts = []
    for doc_file in doc_files:
        with open(doc_file,'r') as f:
            texts.append(f.read())

    bow, dist, rwc, cwc = calculate_vector(texts)

    print "corpus size: {0}, raw word count: {1}, clean word count: {2}".format(len(texts), rwc, cwc)
    print 'done'

