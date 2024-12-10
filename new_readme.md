# Introduction

## PRE-REQUIREMENTS
1. GIT
2. Python/pip
3. Docker

## CLONING
This software was made to learn about good practices and how to create boilerplate code for versatile deploys. It uses Flask and its documented with Swagger. The starting point is almost always the same, i guess this is the point of all this.

    git clone https://github.com/DavidGCalles/Back-Arquetipo

## RUN
Followed by:

    docker-compose up -d

# How it works

## Standalone
NOT DEVELOPED. Story AR-31. You can run:

    run.py

And it will work the same as if you run it from docker, without its niceties. It will run on the development server of Flask and write to a sqlite database that will be erased when finishing the program.

## Docker
It deploy 2 containers, one for the backend, other for the test db. You can test de db connection in:

   http://localhost:5000/swagger

# Demo use
NOT DEVELOPED. Story AR-28. It needs a script to setup couple of tables of the db and populate them with mock data.

# Unordered sections

## List of ENV variables used in the app
1. SWAGGER_HOST: This variable needs to be present when deploying beyond local because if not, not even the basic acces tests wont work

    1.1. This variable is used inside app/routes/main.py in the endpoint @main_bp.route('/swagger.json'). This will select the correct host depending on the deployment type.

