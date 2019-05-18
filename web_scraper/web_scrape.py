#!/bin/python
"""
A script that scrapes a specified website for job posting data.

scrapy runspider web_scrape.py -o links.csv -s CLOSESPIDER_PAGECOUNT=100 -a job_title='software+engineer'
"""
import scrapy


class IndeedJobPostSpider(scrapy.Spider):
    """
    A Scrapy Spider designed to scrape Indeed.com.
    """
    # Parameters
    name = 'indeed'

    def __init__(self, job_title='', **kwargs):
        """
        Override default constructor to parse an extra input arguments.
        :param job_title:
        :param kwargs:
        """
        self.job_title = job_title
        self.start_urls = [f'https://www.indeed.com/jobs?q={job_title}&fromage=7&limit=50']
        super().__init__(**kwargs)

    def parse(self, response):
        # Pull all links related to job postings
        for posting_link in response.css('a::attr(href)').re(r'/rc.*|/company.*|/pagead.*'):
            # Follow each link to collect job posting data
            yield response.follow(posting_link, self.parse_posting_link)

        # Follow to the next page of results indefinitely
        next_page = response.css('a::attr(href)').re(r'.*start=.*')
        if next_page is not None:
            for page in next_page:
                yield response.follow(page, self.parse)

    def parse_posting_link(self, response):
        # Return the URL and the contents of the job posting
        raw_data = response.css('div[id="jobDescriptionText"] *::text').extract()
        yield {
            'Hyperlink': response.request.url,
            'Posting': '\n'.join(raw_data)
        }
