# Introduction

## PRE-REQUIREMENTS
1. GIT
2. Python/pip
3. Docker

## CLONING
This software was made to learn about good practices and how to create boilerplate code for versatile deploys. It uses Flask and its documented with Swagger. The starting point is almost always the same, i guess this is the point of all this.

    git clone https://github.com/DavidGCalles/Back-Arquetipo

## INSTALL
Then go to your prefered terminal and execute:

    pip install -f requirements.txt

## RUN
Followed by:

    docker-compose up -d

## List of ENV variables used in the app
1. SWAGGER_HOST: This variable needs to be present when deploying beyond local because if not, not even the basic acces tests wont work

