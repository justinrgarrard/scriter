"""
Script that does basic preprocessing of data and loads it into storage.
"""

import re
import json
import hashlib
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

FILTER_FILE = 'filter.json'
LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that does basic preprocessing '
                    'of data and loads it into storage.')
    parser.add_argument('input_filename', type=str,
                        help='The filename of inputs to be parsed.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def data_clean(input_filename):
    LOGGER.info('>> Starting data clean.')

    # Load data
    data = pd.read_csv(input_filename)

    # Setup filter
    with open('filter.json', 'r+') as f:
        filter_data = json.load(f)
    filter_out = filter_data['Indeed']
    filter_out_regex = '|'.join(filter_out)
    LOGGER.debug('Filter Regex: {0}'.format(str(filter_out_regex)))

    # Run data through the filter
    data['Posting'] = data['Posting'].apply(lambda x: re.sub(filter_out_regex, '', x, flags=re.IGNORECASE))

    # Hash the URL
    data['URL_Hash'] = data['Hyperlink'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    LOGGER.info('<< Finishing data clean.')
    return data


def data_load(filtered_data, job_title):
    LOGGER.info('>> Starting data load.')
    engine = create_engine('sqlite:///jobscrape.db', echo=False)

    # Create table if it does not exist
    if not engine.dialect.has_table(engine, job_title):
        Base = declarative_base()

        class newTable(Base):
            __tablename__ = job_title
            hyperlink = Column(String)
            posting = Column(String)
            URL_Hash = Column(String, primary_key=True)

        Base.metadata.create_all(engine)

    # Filter out duplicates by URL hash
    hashes = pd.read_sql('SELECT URL_Hash FROM {}'.format(job_title), engine)
    filtered_data_no_dup = filtered_data.loc[~filtered_data['URL_Hash'].isin(hashes['URL_Hash'])]

    # Logging
    LOGGER.debug('Input Data Shape: {0}'.format(filtered_data.shape))
    LOGGER.debug('Filtered Data Shape: {0}'.format(filtered_data_no_dup.shape))
    # LOGGER.debug('Rows to Add (No Duplicates):')
    # LOGGER.debug(filtered_data_no_dup)

    # Dump new rows to DB
    pre_row_count = str(engine.execute("SELECT count(*) FROM {}".format(job_title)).fetchall()[0][0])
    filtered_data_no_dup.to_sql(job_title, con=engine, if_exists='append', index=False)
    post_row_count = str(engine.execute("SELECT count(*) FROM {}".format(job_title)).fetchall()[0][0])

    # Logging
    LOGGER.info('Table Rows Before Insert: {0}'.format(pre_row_count))
    LOGGER.info('Non-Duplicate Rows to Add: {0}'.format(str(len(filtered_data_no_dup))))
    LOGGER.info('Table Rows After Insert: {0}'.format(post_row_count))
    LOGGER.info('Sanity Check: {0} - {1} = {2}'.format(post_row_count, pre_row_count, str(len(filtered_data_no_dup))))
    LOGGER.info('<< Finishing data load.')


if __name__ == '__main__':
    args = parse_args()
    filtered_data = data_clean(args.input_filename)
    data_load(filtered_data, args.job_title)
