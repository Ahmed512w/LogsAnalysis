# Logs Analysis Project
Building an internal reporting tool that will use information from the database to discover what kind of articles
the site's readers like.
This project is a part of the Udacity's Full Stack Web Developer Nanodegree.

## The task
The task is to create a reporting tool that prints out reports (in plain text) based on the data in the database.
This reporting tool is a Python program using the ```psycopg2``` module to connect to the database.
Here are the questions the reporting tool should answer
   1. What are the most popular three articles of all time?
   2. Who are the most popular article authors of all time?
   3. On which days did more than 1% of requests lead to errors?

## System setup
This project makes use of Udacity's Linux-based virtual machine (VM) configuration which includes all of the necessary software to run the application.
1. Download [Vagrant](https://www.vagrantup.com/downloads.html) and install.
2. Download [Virtual Box](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and install. 
3. Download the VM configuration file [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
4. Download the [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) (extract from newsdata.zip) and **LogsAnalysis.py** files from the respository and move them to your **vagrant** directory within your VM.

#### Run these commands from the terminal in the folder where your vagrant is installed in: 
1. ```vagrant up``` to start up the VM.
2. ```vagrant ssh``` to log into the VM.
3. ```cd /vagrant``` to change to your vagrant directory.
4. ```psql -d news -f newsdata.sql``` to load the data and create the tables.
5. ```python3 LogsAnalysis.py``` to run the reporting tool.

## Views used
#### log_article_auther
````sql
CREATE VIEW log_article_auther AS
SELECT log.id AS log,
       articles.slug AS article,
       authors.name  AS author
FROM  log, articles, authors
WHERE log.path = CONCAT( '/article/', articles.slug )
AND   articles.author = authors.id;
````

#### requests
````sql
CREATE VIEW requests AS
SELECT DATE(time) AS day,
       COUNT(*) AS num
FROM   log 
GROUP BY day;
````

#### request_errors
````sql
CREATE VIEW request_errors AS
SELECT DATE(time) AS day,
       COUNT(*) AS num 
FROM  log
WHERE status = '404 NOT FOUND' 
GROUP BY day;
````

#### error_percent
````sql
CREATE VIEW error_percent AS
SELECT requests.day,
       request_errors.num::decimal  /  requests.num::decimal * 100 AS percent
FROM   requests , request_errors
WHERE requests.day = request_errors.day;
````

## Helpful Resources
* [Vagrant](https://www.vagrantup.com/downloads)
* [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* [PEP 8 -- Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
* [The select statement](https://www.postgresql.org/docs/9.5/static/sql-select.html)
* [SQL string functions](https://www.postgresql.org/docs/9.5/static/functions-string.html)
* [Aggregate functions](https://www.postgresql.org/docs/9.5/static/functions-aggregate.html)
