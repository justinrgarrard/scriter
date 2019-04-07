"""
Script that does basic preprocessing of data and loads into storage.
"""

import re
import json
import argparse
import logging
import pandas as pd

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
    data['post_data'] = data['post_data'].apply(lambda x: re.sub(filter_out_regex, '', x, flags=re.IGNORECASE))
    LOGGER.info('Data clean complete.')
    return data


def data_load(clean_data):
    # Temporary stub to spit data back out into a file
    clean_data.to_csv('out.csv', index=False)


if __name__ == '__main__':
    args = parse_args()
    clean_data = data_clean()
    data_load(clean_data)
