# README

Scriter is a web application that scrapes job posting data from various
websites and visualizes the outputs on a server.


### Architecture

For prototyping purposes, the following three components run on the
same server.

* Weekly Web Scraper Job to Gather Data (Python + cron)

* DB to Store Data (Postgres)

* Web Server to Display Data (Apache)


### Development Status

**Data Load**

| Status  | Task |
|---|---|
| Done | Basic Web Scraper |
| Done | Data Cleaning Process |
| TBD | Database Setup |
| TBD | Database Load Process |
| TBD | Cron Web Scrape |


