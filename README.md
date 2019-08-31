# README

Scriter is a web application that scrapes job posting data and visualizes
the outputs.


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

4. Run the Ansible playbook to install and configure Scriter

```
# cd setup/
# ansible-playbook main.yml --become
```

### Usage

1. Collect data using the web scraper

```
[scriter]$ cd web_scraper/
[scriter]$ scrapy runspider web_scrape.py -o links.csv -s CLOSESPIDER_PAGECOUNT=100 -a job_title='software+engineer'
```

2. Load data into the Postgres DB

```
[scriter]$ cd web_scraper/
[scriter]$ python data_load.py links.csv software_engineer
```

3. Perform data transformations

```
[scriter]$ cd data_modeler/
[scriter]$ python model_build.py software_engineer
```

4. Launch web server

```
[scriter]$ cd web_server/
[scriter]$ python manage.py runserver
```

