"""
Script that converts job posting data into NLP models.
"""

import re
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine
from nltk import tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()

problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n()-:]')
sharps = re.compile(r'#')
doubleplus = re.compile(r'\+\+')
doublespace = re.compile(r' {2}')
stopWords = set(stopwords.words('english'))


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
    # posting_data = posting_data.apply(lambda x: re.sub(sharps, 'sharp', x))
    # posting_data = posting_data.apply(lambda x: re.sub(doubleplus, 'doubleplus', x))

    # Fit the data with sklearn's model
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    aleph = vectorizer.fit_transform(posting_data)

    print(aleph[0, vectorizer.vocabulary_['python']])
    # print(aleph[0, vectorizer.vocabulary_['csharp']])


if __name__ == '__main__':
    args = parse_args()
    main(args.job_title)
