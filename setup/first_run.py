"""
First run script, which populates the databases for the web server.
"""

import os
import argparse
import subprocess
import logging

LOG_FORMAT = '%(asctime)s: %(filename)s [%(funcName)s]- %(message)s'
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
LOGGER = logging.getLogger()
TECH_LISTING = 'tech.json'
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
INGEST_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_ingest'.format(DB_USER, DB_PASS)
MODEL_DB_CONN_STR = 'postgresql://{0}:{1}@localhost/scriter_web'.format(DB_USER, DB_PASS)
JOB_TITLES = ["Software Developer",
                "Front End Developer",
                "Back End Developer",
                "Full Stack Developer",
                "Game Developer",
                "Software Engineer",
                "Firmware Engineer",
                "Data Engineer",
                "DevOps Engineer",
                "Data Analyst",
                "Data Scientist",
                "System Administrator",
                "Linux Administrator",
                "Network Administrator"]


def parse_args():
    """
    Parse input arguments.

    :return: args: A Dictionary-like object that stores input parameters as attributes.
    """
    parser = argparse.ArgumentParser(
        description='Script that populates databases for the Scriter web server.')
    return parser.parse_args()


def web_scrape():
    """
    Run the web scraper on each job title.

    :return:
    """
    target_dir = '../web_scraper'
    for job in JOB_TITLES:
        cmd = "scrapy runspider web_scrape.py -o {0}.csv -s CLOSESPIDER_PAGECOUNT=1000" \
              " -a job_title='{1}'  >> ../test/run_log.txt 2>&1".format(job.replace(' ', '_'), job.replace(' ', '+'))
        LOGGER.info(cmd)
        output = subprocess.check_output(cmd, cwd=target_dir, shell=True)
        LOGGER.info(output)


def data_load():
    """
    Load web scraper data for each job title.

    :return:
    """
    target_dir = '../web_scraper'
    for job in JOB_TITLES:
        cmd = "python data_load.py {0}.csv {1} >> ../test/run_log.txt 2>&1".format(job.replace(' ', '_'), job.lower().replace(' ', '_'))
        LOGGER.info(cmd)
        output = subprocess.check_output(cmd, cwd=target_dir, shell=True)
        LOGGER.info(output)


def model_build():
    """
    Generate statistics for each job title.
    
    :return:
    """
    target_dir = '../data_modeler'
    for job in JOB_TITLES:
        cmd = "python model_build.py {0} >> ../test/run_log.txt 2>&1".format(job.lower().replace(' ', '_'))
        LOGGER.info(cmd)
        output = subprocess.check_output(cmd, cwd=target_dir, shell=True)
        LOGGER.info(output)


if __name__ == '__main__':
    args = parse_args()
    web_scrape()
    data_load()
    model_build()
