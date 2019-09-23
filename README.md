# README

[Scriter](http://www.scriter.net) is a web application that scrapes job posting data and visualizes
the outputs.


### Architecture

The application is written in Python and consists of four separate components, loosely coupled.

* Web Scraper Job to Gather Data (Scrapy)

* DB to Store Data (Postgres)

* Model Builder to convert raw job posting text into TFIDF metrics (Sklearn)

* Web Server to Display Data (Django)

![Visual of Architecture](scriter_overview.png)

### First Time Setup

An installer has been provided to simplify the initial setup. Use the following
steps to configure an Ubuntu 18.04 server.

1. Become root

```
[user]$ sudo su
```

2. Install Ansible

```
[root]# apt-get install ansible
```

3. Clone this repository at /opt/scriter

```
[root]# cd /opt
[root]# git clone https://github.com/justinrgarrard/scriter.git
```

4. Run the Ansible playbook to install and configure the application

```
[root]# cd /opt/scriter/setup/
[root]# ansible-playbook install.yml
```

5. Perform a first time data load
```
[root]# sudo su scriter
[scriter]$ cd /opt/scriter/test/
[scriter]$ python first_run.py
```

6. (Optional) Test deploy to localhost
```
[scriter]$ cd /opt/scriter/web_server/
[scriter]$ python manage.py runserver
< CTRL-C to Kill>
```

7. Deploy
```
[scriter]$ cd /opt/scriter/setup/
[scriter]$ ansible deploy.yml
```

### Manual Usage

1. Collect data using the web scraper

```
[scriter]$ cd web_scraper/
[scriter]$ scrapy runspider web_scrape.py -o software_engineer.csv -s CLOSESPIDER_PAGECOUNT=1000 -a job_title='software+engineer'
```

2. Load data into the Postgres DB

```
[scriter]$ cd web_scraper/
[scriter]$ python data_load.py software_engineer.csv software_engineer
```

3. Generate TFIDF metrics

```
[scriter]$ cd data_modeler/
[scriter]$ python model_build.py software_engineer
```

