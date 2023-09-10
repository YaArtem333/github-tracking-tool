# Github tracking tool

## Overview
This is REST Api service which is made to help GitHub users!

With this tool you can track changes in any accounts or repositories 
on GitHub. It can show changes in the selected time periods, which is very
helpful, if you want to watch someone's actions ir account changes.
This tool can help for example team leaders who want to know, what were 
the changes in the project in selected period and who made them. With
this tool everybody can do it just in few seconds.

API documentation is in the file  ***swagger_api_documentation.yml***

## Stack

+ Python 3.10
+ Flask 2.3.2
+ MongoDB
+ Docker
+ pytest
+ unit-test
  
## Preparation

You need to have: 
+ MongoDB on your machine
+ Python 3.10 
+ Docker / ***make*** utilite for running Makefile

## Install & Run

### Run with Docker

**Copy repository**
```shell
git clone https://github.com/YaArtem333/github-tracking-tool
```

**Create and run docker container**
```shell
docker-compose up
```
The service is available

### Run on your computer with ***make*** ###

**Copy repository**
```shell
git clone https://github.com/YaArtem333/github-tracking-tool
```

**Change database parameters**

1) Open file /app/models.py
2) Change parameters:
```shell
client = MongoClient('mongodb', 27017) # write your host insted of mongodb
#for example: client = MongoClient('127.0.0.1', 27017)
```

**install needed libraries & run**
```shell
make run
```

**if you want to run tests:**
```shell
make tests
```

**if you want to run tests with coverage:**
```shell
make coverage
```

The service is available