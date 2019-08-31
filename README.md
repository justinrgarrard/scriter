# README

Scriter is a web application that scrapes job posting data from various
websites and visualizes the outputs on a server.


### Architecture

For prototyping purposes, the following three components run on the
same server.

* Weekly Web Scraper Job to Gather Data (Python + cron)

* DB to Store Data (Postgres)

* Web Server to Display Data (Apache + Django)

![Visual of Architecture](scriter_overview.png)

### Setup

1. Become root

```
[user]$ sudo su
```

2. Install Ansible on an Ubuntu 18.04 Server

```
# apt-get install ansible
```

3. Clone this repository at /opt/scriter

```
# cd /opt
# git clone https://github.com/justinrgarrard/scriter.git
```

4. Run the Ansible playbook in setup/ to install and configure Scriter

```
# cd /setup
# ansible-playbook main.yml --become
```

### Usage

1. Collect data using the web scraper

```
[scriter]$ scrapy runspider web_scrape.py -o links.csv -s CLOSESPIDER_PAGECOUNT=100 -a job_title='software+engineer'
```

2. Load data into the Postgres DB

```
[scriter]$ python data_load.py links.csv software_engineer
```

3. Perform data transformations

```
python model_build.py software_engineer
```

4. Launch web server

```
python manage.py runserver
```

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
| TBD | Polish web appearance |
| TBD | Parametrize for different job titles |
| TBD | Deploy site to scriter.net domain |


**Functional**

| Status  | Task |
|---|---|
| DONE | Reorganize file structure by component |
| TBD | Develop test suite |
| DONE | Swap SQLite for PostgreSQL |
| DONE | Properly handle DB credentials |
| DONE | Ansible file for server setup |
| TBD | Investigate containerization |
