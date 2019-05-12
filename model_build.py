"""
Script that converts job posting data into NLP models.
"""

import json
import logging
import argparse
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import CountVectorizer

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that converts job posting data into NLP models.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def main(job_title):
    LOGGER.info('>>>Beginning model build.')
    # Get a listing of common technologies,
    # per StackOverflow's 2019 survey
    with open('tech.json', 'r+') as f:
        techs = json.load(f)

    # Pull data from table
    engine = create_engine('sqlite:///jobscrape.db', echo=False)
    posting_data = pd.read_sql(job_title, engine)['Posting']
    LOGGER.info('Input Data Shape:')
    LOGGER.info(posting_data.shape)

    # Generate statistics on data
    vocab = [key.lower() for key in techs]
    LOGGER.info('Number of Keywords:')
    LOGGER.info(len(vocab))
    vectorizer = CountVectorizer(ngram_range=(1, 2), strip_accents='unicode',
                                 vocabulary=vocab)
    count_vector = vectorizer.fit_transform(posting_data)

    ## Total Counts (Term Frequency; TF)
    counts = {key: count_vector[val].sum() for key, val in vectorizer.vocabulary_.items()}
    sorted_counts = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    LOGGER.info('Term Frequencies:')
    LOGGER.info(sorted_counts)

    ## Unique Counts (Document Frequency; DF)
    uniq_counts = {key: count_vector[val].count_nonzero() for key, val in vectorizer.vocabulary_.items()}
    sorted_uniq_counts = sorted(uniq_counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
    LOGGER.info('Document Frequencies:')
    LOGGER.info(sorted_uniq_counts)

    ## Inverse Document Frequency (IDF)
    ### Traditional: log( N / DF )
    ### Smoothed: log( N+1 / DF+1 )
    num_documents = len(posting_data)
    idf_vals = {key: np.log((num_documents+1) / (uniq_counts[key]+1)) for key in vectorizer.vocabulary_}
    sorted_idf_vals = sorted(idf_vals.items(), key=lambda x: (x[1], x[0]), reverse=True)
    LOGGER.info('Inverse Document Frequencies:')
    LOGGER.info(sorted_idf_vals)

    ## Term Frequency * Inverse Document Frequency (TFIDF)
    tfidf_vals = {key: counts[key] * idf_vals[key] for key in vectorizer.vocabulary_}
    sorted_tfidf_vals = sorted(tfidf_vals.items(), key=lambda x: (x[1], x[0]), reverse=True)
    LOGGER.info('TFIDF Values:')
    LOGGER.info(sorted_tfidf_vals)

    # Format output
    output = pd.DataFrame()
    output['Keyword'] = vocab
    output['TF'] = output['Keyword'].apply(lambda x: counts[x])
    output['DF'] = output['Keyword'].apply(lambda x: uniq_counts[x])
    output['IDF'] = output['Keyword'].apply(lambda x: idf_vals[x])
    output['TFIDF'] = output['Keyword'].apply(lambda x: tfidf_vals[x])
    output['Document Count'] = num_documents

    LOGGER.info('Output Data Shape:')
    LOGGER.info(output.shape)

    # Store output
    engine2 = create_engine('sqlite:///jobmodel.db', echo=False)
    output.to_sql(job_title, con=engine2, if_exists='replace', index=False)

    LOGGER.info('<<<Finished model build.')


if __name__ == '__main__':
    args = parse_args()
    main(args.job_title)
