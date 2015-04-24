#
# Auto Text Bin Plus
#

import numpy as np

import nltk
import re

from sklearn.feature_extraction.text import CountVectorizer

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

def build_bag_of_words(clean_text, build_dist=False):

    # Initializ the bag-of-words tool
    vectorizer = CountVectorizer(
        analyzer = "word",
        tokenizer = None,
        preprocessor = None,
        stop_words = None,
        max_features = 5000
    )

    # perform the transform
    data_features = vectorizer.fit_transform(clean_text).toarray()

    dist = None
    if build_dist == True:
       dist = []
       _d = np.sum(data_features, axis=0)
       vocab = vectorizer.get_feature_names()
       for tag, count in zip(vocab, _d):
           dist.append((count, tag))

    return data_features, dist

def autobin(texts):
    
    clean_texts = []
    for text in texts:

        ct = clean_text(text)
        
        print "Text:"
        print text
        print ct
        print ''

        clean_texts.append(ct)

    bow, dist = build_bag_of_words(clean_texts, build_dist=True)

    print "\nBag of Words:"
    print bow

    print "\nDistribution of Words:"
    print dist

if __name__ == '__main__':

    texts = [
        "Never have I found a man as dedicated to such a worthless cause as much as self doubt.",
        "How perfect must a day be to classify as the MOST perfect.",
        "I like turtles.",
    ]

    autobin(texts)

