"""
Script that converts job posting data into NLP models.
"""

import us
import re
import logging
import argparse
import pandas as pd
from collections import defaultdict
from sqlalchemy import create_engine
from nltk import tokenize
from nltk import TweetTokenizer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

from collections import Counter

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()

# problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n()-:]')
# sharps = re.compile(r'#')
# doubleplus = re.compile(r'\+\+')
# doublespace = re.compile(r' {2}')
# stopWords = set(stopwords.words('english'))


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that converts job posting data into NLP models.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def main(job_title):
    # Pull data from table
    engine = create_engine('sqlite:///jobscrape.db', echo=False)
    posting_data = pd.read_sql(job_title, engine)['Posting']
    print(posting_data.shape)

    # Do some preprocessing
    ## Remove state names
    st = us.states.mapping('abbr', 'name')
    state_names = set(st.keys()).union(st.values())
    state_names = re.compile('|'.join(state_names))
    posting_data = posting_data.apply(lambda x: re.sub(state_names, '', x))

    # Fit the data with sklearn's model, cutting out phrases that appear too frequently
    vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_df=0.85, strip_accents='unicode')
    vector = vectorizer.fit_transform(posting_data)

    print(vector.shape)
    print(vector[0, vectorizer.vocabulary_['python']])
    print(vector[0, vectorizer.vocabulary_['java']])
    # print(aleph[0, vectorizer.vocabulary_['csharp']])

    # Find the highest ranked phrases
    aleph = vectorizer.get_feature_names()
    beta = sorted([(gram, vector[0, vectorizer.vocabulary_[gram]]) for gram in aleph], key=lambda x: x[1], reverse=True)
    delta = pd.DataFrame(beta, columns=['Gram', 'TFIDF'])
    print(delta)


if __name__ == '__main__':
    args = parse_args()
    main(args.job_title)
