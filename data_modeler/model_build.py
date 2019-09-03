"""
Script that converts job posting data into NLP models.

python model_build.py software_engineer
"""

import os
import json
import logging
import argparse
import numpy as np
import pandas as pd
from django.db import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.feature_extraction.text import CountVectorizer

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()
TECH_LISTING = 'tech.json'
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
INGEST_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_ingest'.format(DB_USER, DB_PASS)
MODEL_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_web'.format(DB_USER, DB_PASS)
MODEL_DB_NAME = 'posting_statistics'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that converts job posting data into NLP models.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def get_filepath(input_filename):
    """

    :param input_filename:
    :return:
    """
    input_filepath = os.path.dirname(os.path.abspath(__file__))
    input_filepath = os.path.join(input_filepath, input_filename)
    return input_filepath


def main(job_title):
    LOGGER.info('>>>Beginning model build.')
    tech_filepath = get_filepath(TECH_LISTING)
    with open(tech_filepath, 'r+') as f:
        techs = json.load(f)

    # Pull data from table
    engine = create_engine(INGEST_DB_CONN_STR)
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
    output['DOCUMENT_COUNT'] = num_documents
    output['JOB_TITLE'] = job_title

    LOGGER.info('Output Data Shape:')
    LOGGER.info(output.shape)

    # Replace old entries with new entries
    engine2 = create_engine(MODEL_DB_CONN_STR)
    # Session = sessionmaker(bind=engine2)
    # session = Session()
    #
    # ## Hate to duplicate code like this, is there a fancy import
    # ## that will work more smoothly?
    # class Job(models.Model):
    #     class Meta:
    #         db_table = 'posting_statistics'
    #         managed = False
    #
    #     Keyword = models.CharField(max_length=100)
    #     TF = models.IntegerField()
    #     DF = models.IntegerField()
    #     IDF = models.FloatField()
    #     TFIDF = models.FloatField()
    #     DOCUMENT_COUNT = models.IntegerField()
    #     JOB_TITLE = models.CharField(max_length=100)
    #
    # old = session.query(Job).filter(JOB_TITLE=job_title)
    output.to_sql(MODEL_DB_NAME, con=engine2, if_exists='append', index_label='id')

    LOGGER.info('<<<Finished model build.')


if __name__ == '__main__':
    args = parse_args()
    main(args.job_title)
