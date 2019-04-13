"""
Script that does basic preprocessing of data and loads into storage.
"""

import re
import json
import hashlib
import logging
import argparse
import pandas as pd
from sqlalchemy import create_engine

logging.basicConfig(format='%(asctime)s: %(filename)s [%(funcName)s]- %(message)s', level=logging.DEBUG)
LOGGER = logging.getLogger()
FILTER_FILE = 'filter.json'


def parse_args():
    parser = argparse.ArgumentParser(
        description='Script that does basic preprocessing '
                    'of data and loads into storage.')
    return parser.parse_args()


def data_clean():
    LOGGER.info('>> Starting data clean.')

    # Load data
    data = pd.read_csv('links.csv')

    # Setup filter
    with open('filter.json', 'r+') as f:
        filter_data = json.load(f)
    filter_out = filter_data['Indeed']
    filter_out_regex = '|'.join(filter_out)
    LOGGER.debug('Filter Regex: {0}'.format(str(filter_out_regex)))

    # Run data through the filter
    data['Posting'] = data['Posting'].apply(lambda x: re.sub(filter_out_regex, '', x, flags=re.IGNORECASE))
    LOGGER.info('<< Finishing data clean.')
    return data


def data_load(filtered_data):
    LOGGER.info('>> Starting data load.')

    # Make a hash from the URL
    filtered_data['URL_Hash'] = filtered_data['Hyperlink'].apply(lambda x: hashlib.md5(x.encode()).hexdigest())

    # Filter out duplicates by URL hash
    engine = create_engine('sqlite:///jobscrape.db', echo=False)
    hashes = pd.read_sql('SELECT URL_Hash FROM posting_data', engine)
    filtered_data_no_dup = filtered_data.loc[~filtered_data['URL_Hash'].isin(hashes['URL_Hash'])]

    # Logging
    LOGGER.debug('Input Data Shape: {0}'.format(filtered_data.shape))
    LOGGER.debug('Filtered Data Shape: {0}'.format(filtered_data_no_dup.shape))
    LOGGER.debug('Rows to Add (No Duplicates):')
    LOGGER.debug(filtered_data_no_dup)

    # Dump new rows to DB
    pre_row_count = str(engine.execute("SELECT count(*) FROM posting_data").fetchall()[0][0])
    filtered_data_no_dup.to_sql('posting_data', con=engine, if_exists='append')
    post_row_count = str(engine.execute("SELECT count(*) FROM posting_data").fetchall()[0][0])

    # Logging
    LOGGER.info('Pre Insert Table Row Count: {0}'.format(pre_row_count))
    LOGGER.info('Non-Duplicate Rows to Add: {0}'.format(str(len(filtered_data_no_dup))))
    LOGGER.info('Post Insert Table Row Count: {0}'.format(post_row_count))
    LOGGER.info('Sanity Check: {0} - {1} = {2}'.format(post_row_count, pre_row_count, str(len(filtered_data_no_dup))))
    LOGGER.info('<< Finishing data load.')


if __name__ == '__main__':
    args = parse_args()
    filtered_data = data_clean()
    data_load(filtered_data)
