# Dev Log

### Development Status

**Data Load**

| Status  | Task |
|---|---|
| Done | Basic Web Scraper |
| Done | Data Cleaning Process |
| Done | Temporary Database Setup |
| Done | Database Load Process |
| Done | Parametrize Web Scrape (Job Title) |
| TBD | Cron Web Scrape |
| TBD | Parametrize for Multiple Sources |


**Data Access**

| Status  | Task |
|---|---|
| DONE | Query database |
| DONE | Create a TF-IDF model |
| DONE | Store the TF-IDF model |
| DONE | Refine the TF-IDF model |
| TBD | Aggregate synonyms (i.e. JS and JavaScript) |


**Web Stack**

| Status  | Task |
|---|---|
| DONE | Create locally hosted site |
| DONE | Load data into web server DB |
| DONE | Visualize TF-IDF models |
| DONE | Develop UI model |
| WIP | Parametrize for different job titles |
| TBD | Deploy site to scriter.net domain |


**Functional**

| Status  | Task |
|---|---|
| DONE | Reorganize file structure by component |
| TBD | Develop test suite |
| DONE | Swap SQLite for PostgreSQL |
| DONE | Properly handle DB credentials |
| DONE | Ansible file for server setup |


** Ideas **
| TBD | Investigate Containerization |
| TBD | Date Range Sort |
| TBD | Text Similarity Filter for Improved Duplicate Detection |


### History

**Scriter 1.0**

* A static web application hosted on an AWS S3 bucket. 

* Custom scraping logic using urllib and Beautiful Soup

* Custom cleaning logic using Pandas and NLTK

* Basic hand-coded HTML and CSS

* Graphs generated with Matplotlib

My first attempt at a start-to-finish data pipeline. I had some
experience with data processing, but there were a lot of new
technologies to pick up. Web scraping, web dev, and AWS hosting were all
first time experiences. 


**Scriter 2.0**

* Converted to a single page application using vanilla JS

* Added Bootstrap 

* Various fixes to cleaning and scraping logic

For this iteration, I wanted to get a better handle on web dev
technology. My focus was on learning how Javascript integrates with
the rest of a web page. Bootstrap came up with enough frequency to
justify a detour.


**Scriter 3.0 (current)**

* Rewrite of scraping logic to use Scrapy

* Store results persistently in a database

* Host from a full web server

* Use a TF-IDF model instead of a unique frequency counter

A production grade data pipeline application. This incarnation makes
use of databases, web frameworks, and Ansible. The increased emphasis
on infrastructure stems from work experience as a Hadoop Admin.


### Chickenscratch

#### Django

Django may not have been the best fit for a front-end framework. I had
hoped to use one table per job title in web server, but there doesn't seem
to be an easy way to implement that.
