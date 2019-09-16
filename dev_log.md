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
| DONE | Parametrize for different job titles |
| WIP | Deploy site to scriter.net domain |


**Functional**

| Status  | Task |
|---|---|
| DONE | Reorganize file structure by component |
| DONE | Develop basic test suite |
| DONE | Swap SQLite for PostgreSQL |
| DONE | Properly handle DB credentials |
| DONE | Ansible file for server setup |


** Ideas **
| TBD | Investigate Containerization |
| TBD | Date Range Sort |
| TBD | Text Similarity Filter for Improved Duplicate Detection |
| TBD | More Thorough Test Suite |
| TBD | Automatically update HTML with table names from DB |


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
on infrastructure stems from my work experience as a Hadoop Admin.


### Chickenscratch

#### Django

Django may not have been the best fit for a front-end framework. I had
hoped to use one table per job title in web server, but there doesn't seem
to be an easy way to implement that.

#### NLTK, CountVectorizer, TfidfVectorizer, and TfidfTransformer

Having had some prior experience with NLTK, I wanted to try sklearn's tooling
for a common NLP task. I like the way their framework is organized. All the
components have consistent function names, and the documentation is top notch.

That being said, I was a little disappointed that there was no easy way to pull
term frequencies or document frequencies from the vectorizer tools. I wound up
implementing that functionality by scratch. Doing so gave me the urge to do IDF
and TFIDF from the ground-up. Not necessarily the most efficient use of time, but
it felt good to do the basics by hand. I'm sure there are also some losses in runtime
speed.
