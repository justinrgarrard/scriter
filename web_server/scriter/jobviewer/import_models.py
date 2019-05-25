"""
A script to import data models into the web server database.
"""

import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine

from .models import Job

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that imports data from the model builder DB'
                    'into the web server DB.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def main(job_title):
    # Connect to database
    engine = create_engine('postgresql://roy@localhost/scriter_jobs')

    # Remove contents of web server's models

    # Pull data from data modeler
    model_data = pd.read_sql(job_title, engine)
    LOGGER.info('Input Data Shape:')
    LOGGER.info(model_data.shape)

    # Create model objects
    model_objects = [Job(x['Keyword'], x['TF'], x['DF'], x['IDF'], x['TFIDF'], x['Document Count']) for x in model_data]
    LOGGER.info(model_objects[0:5])

    # output = pd.DataFrame()
    # output['Keyword'] = vocab
    # output['TF'] = output['Keyword'].apply(lambda x: counts[x])
    # output['DF'] = output['Keyword'].apply(lambda x: uniq_counts[x])
    # output['IDF'] = output['Keyword'].apply(lambda x: idf_vals[x])
    # output['TFIDF'] = output['Keyword'].apply(lambda x: tfidf_vals[x])
    # output['Document Count'] = num_documents
    #
    #
    #
    # KEYWORD = models.CharField(max_length=100)
    # TF = models.IntegerField()
    # DF = models.IntegerField()
    # IDF = models.FloatField()
    # TFIDF = models.FloatField()
    # DOCUMENT_COUNT = models.IntegerField


if __name__ == '__main__':
    args = parse_args()
    main(args.job_title)
