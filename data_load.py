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
    LOGGER.info('Starting data clean.')

    # Load data
    data = pd.read_csv('links.csv')

    # Setup filter
    with open('filter.json', 'r+') as f:
        filter_data = json.load(f)
    filter_out = filter_data['Indeed']
    filter_out_regex = '|'.join(filter_out)
    LOGGER.debug('Filter Regex')
    LOGGER.debug(str(filter_out_regex))

    # Run data through the filter
    data['Posting'] = data['Posting'].apply(lambda x: re.sub(filter_out_regex, '', x, flags=re.IGNORECASE))
    LOGGER.info('Data clean complete.')
    return data


def data_load(filtered_data):
    # filtered_data['URL_Hash'] = filtered_data['Hyperlink'].apply(lambda x: hashlib.md5(x.encode()))

    # Temporary stub to spit data back out into a file
    filtered_data.to_csv('out.csv', index=False)

    # Dump to DB
    engine = create_engine('sqlite://', echo=False)
    filtered_data.to_sql('posting_data', con=engine)

    x = engine.execute("SELECT * FROM posting_data limit 100").fetchall()
    LOGGER.info(str(x))


if __name__ == '__main__':
    args = parse_args()
    filtered_data = data_clean()
    data_load(filtered_data)
