"""
Script that does basic preprocessing of data and loads it into storage.

python data_load.py links.csv software_engineer
"""

import os
import re
import json
import hashlib
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

FILTER_FILE = 'filter.json'
LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
INGEST_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_ingest'.format(DB_USER, DB_PASS)


def parse_args():
    """
    Parse input arguments.

    :return: args: A Dictionary-like object that stores input parameters as attributes.
    """
    parser = argparse.ArgumentParser(
        description='Script that does basic preprocessing '
                    'of data and loads it into storage.')
    parser.add_argument('input_filename', type=str,
                        help='The filename of inputs to be parsed.')
    parser.add_argument('job_title', type=str,
                        help='The job title tied to the data; used to '
                             'determine the database name.')
    return parser.parse_args()


def get_filepath(input_filename):
    """
    Helper function that gets the full path of a file, given its filename.

    :param input_filename:
    :return:
    """
    input_filepath = os.path.dirname(os.path.abspath(__file__))
    input_filepath = os.path.join(input_filepath, input_filename)
    return input_filepath


def data_clean(input_filename):
    """
    Load data from file, removing unnecessary boilerplate from the HTML.

    :param input_filename: The filename, as a String.
    :return: data: A Dictionary containing cleaned extracts from the input file.
    """
    LOGGER.info('>> Starting data clean.')

    # Load data
    input_filepath = get_filepath(input_filename)
    data = pd.read_csv(input_filepath)

    # Set up filter
    filter_filepath = get_filepath(FILTER_FILE)
    with open(filter_filepath, 'r+') as f:
        filter_data = json.load(f)
    filter_out = filter_data['Indeed']
    filter_out_regex = '|'.join(filter_out)
    LOGGER.debug('Filter Regex: {0}'.format(str(filter_out_regex)))

    # Filter data
    data['Posting'] = data['Posting'].apply(lambda x: re.sub(filter_out_regex, '', str(x), flags=re.IGNORECASE))

    # Hash the URL
    data['URL_Hash'] = data['Hyperlink'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    LOGGER.info('<< Finishing data clean.')
    return data


def data_load(filtered_data, job_title):
    """
    Store filtered data in a relational database.

    :param filtered_data: A Dictionary containing cleaned extracts from the input file.
    :param job_title: The job title affiliated with this posting.
    :return: None.
    """
    LOGGER.info('>> Starting data load.')

    # Open connection to database
    engine = create_engine(INGEST_DB_CONN_STR)

    # Create table for job title if it does not exist
    if not inspect(engine).has_table(job_title):
        Base = declarative_base()

        class newTable(Base):
            __tablename__ = job_title
            Hyperlink = Column(String)
            Posting = Column(String)
            URL_Hash = Column(String, primary_key=True)

        Base.metadata.create_all(engine)

    # Filter out duplicates by URL hash
    hashes = pd.read_sql('SELECT "URL_Hash" FROM {}'.format(job_title), engine)
    filtered_data_no_dup = filtered_data.loc[~filtered_data['URL_Hash'].isin(hashes['URL_Hash'])]
    LOGGER.debug('Input Data Shape: {0}'.format(filtered_data.shape))
    LOGGER.debug('Filtered Data Shape: {0}'.format(filtered_data_no_dup.shape))

    # # Dump new rows to database
    pre_row_count = str(engine.execute("SELECT count(*) FROM {}".format(job_title)).fetchall()[0][0])
    filtered_data_no_dup.to_sql(job_title, con=engine, if_exists='append', index=False)
    post_row_count = str(engine.execute("SELECT count(*) FROM {}".format(job_title)).fetchall()[0][0])

    # Log transaction details
    LOGGER.debug('Table Rows Before Insert: {0}'.format(pre_row_count))
    LOGGER.info('Non-Duplicate Rows to Add: {0}'.format(str(len(filtered_data_no_dup))))
    LOGGER.debug('Table Rows After Insert: {0}'.format(post_row_count))
    LOGGER.debug('Sanity Check: {0} - {1} = {2}'.format(post_row_count, pre_row_count, str(len(filtered_data_no_dup))))
    LOGGER.info('<< Finishing data load.')


if __name__ == '__main__':
    args = parse_args()
    filtered_data = data_clean(args.input_filename)
    data_load(filtered_data, args.job_title)
