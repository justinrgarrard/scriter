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
    LOGGER.info('Input Data Shape: {0}'.format(filtered_data.shape))
    LOGGER.info('Input Data Schema: {0}'.format(filtered_data.columns))
    # filtered_data['URL_Hash'] = filtered_data['Hyperlink'].apply(lambda x: hashlib.md5(x.encode()))

    # Temporary stub to spit data back out into a file
    # filtered_data.to_csv('out.csv', index=False)

    # Dump to DB
    engine = create_engine('sqlite:///jobscrape.db', echo=False)

    x = engine.execute("SELECT count(*) FROM posting_data").fetchall()
    LOGGER.info('Pre Insert Table Row Count: {0}'.format(str(x)))

    filtered_data.to_sql('posting_data', con=engine, if_exists='replace')

    x = engine.execute("SELECT count(*) FROM posting_data").fetchall()
    LOGGER.info('Post Insert Table Row Count: {0}'.format(str(x)))
    LOGGER.info('<< Finishing data load.')


if __name__ == '__main__':
    args = parse_args()
    filtered_data = data_clean()
    data_load(filtered_data)
