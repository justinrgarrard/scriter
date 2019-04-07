#!/bin/python
"""
A script that scrapes a specified website for job posting data.

scrapy runspider web_scrape.py -o links.csv -s CLOSESPIDER_PAGECOUNT=100
"""
import scrapy


class IndeedJobPostSpider(scrapy.Spider):
    """
    A Scrapy Spider designed to scrape Indeed.com.
    """
    # Parameters
    name = 'indeed'
    title = 'software+engineer'
    start_urls = ['https://www.indeed.com/jobs?q=' + title]

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
        raw_data = response.css('div *::text').extract()
        yield {
            'hyperlink': response.request.url,
            'post_data': '\n'.join(raw_data),
            'source': 'indeed'
        }
