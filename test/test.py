"""
A test suite script for assessing basic functionality and use cases.
"""

import os
import shutil
import unittest
import subprocess


class TestWebScrape(unittest.TestCase):
    def test_run(self):
        """
        Basic Completion
        :return:
        """
        cmd = "scrapy runspider web_scrape.py -o test.csv -s CLOSESPIDER_PAGECOUNT=50 -a job_title='software+engineer'"
        output = subprocess.check_output(cmd, cwd='../web_scraper', shell=True)
        self.assertTrue(os.path.exists('../web_scraper/test.csv'))
        os.remove('../web_scraper/test.csv')

    def test_scrape_count(self):
        """
        CLOSESPIDER_PAGECOUNT ~ Output Count
        :return:
        """
        pass


class TestDataLoad(unittest.TestCase):
    def test_run(self):
        """
        Basic Completion
        :return:
        """
        pass

    def test_scrape_count(self):
        """
        Input Shape ~ Output Shape
        :return:
        """
        pass

    def test_scrape_count_duplicates(self):
        """
        Duplicate Detection
        :return:
        """
        pass


class TestModelBuild(unittest.TestCase):
    def test_run(self):
        """
        Basic Completion
        :return:
        """
        pass

    def test_expected_metrics(self):
        """
        Sample Metrics ~ Expected Metrics
        :return:
        """
        pass


class TestWebServer(unittest.TestCase):
    def test_run(self):
        """
        Basic Completion
        :return:
        """
        pass

    def test_ui(self):
        """
        Basic UI Functionality
        :return:
        """
        pass


if __name__ == '__main__':
    unittest.main()
