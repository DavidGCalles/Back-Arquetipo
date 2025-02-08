# Introduction

## PRE-REQUIREMENTS
1. GIT
2. Python/pip
3. Docker

## CLONING

    git clone https://github.com/DavidGCalles/Back-Arquetipo

## STANDARD RUN METHOD
Followed by:

    docker-compose up -d

# Ways to Run It

## Standalone
You can run:

    run.py

And it will work the same as if you run it from docker, without its niceties. It will run on the development server of Flask and write to a sqlite inmemory database that will be erased when finishing the program.

## Docker
    docker-compose up -d
    
It deploy 2 containers, one for the backend, other for the test db. You can test de db connection in:

   http://localhost:5000/swagger


# How to deploy to Cloud Run

You can find a running prototype here. You can't do much because db connections are not configured yet on cloud:

https://back-arquetipo-856517455627.europe-southwest1.run.app/swagger

## Prerequisites
1. Check if the container builds and runs locally. This step is very important, because you can avoid a lot of headaches knowing for sure your build runs.

## Cloud Run

1. Go to: https://console.cloud.google.com/run
1. Select your project.
1. Click on deploy container and then service, service
1. Implement from Github

### Core Configuration
1. Configure minimal Cloud Build (is mandatory)
    1. Connect your github if its not connected.
    1. Select the repository (the fork of the arquetype on which the app is developed)
    1. Push Next. Select Dockerfile build type
1. Configure name and region (important on pricing and time response)
    1. With auth, we select allow unauthenticated invocations because we want the service to be public.
1. Select CPU allocation and scaling. Its an important section because it has influence in pricing and time response.
    1. Take care with autoscaling. If you set it to 1, you will always have 1 instance up.

### Container, volumes, networking, security

#### Settings

#### Variables and secrets

#### Volume Mounts

#### Cloud SQL connections

Create service.

This will create the cloud build trigger and the cloud run function as service.


# Unordered sections

## List of ENV variables used in the app
1. SWAGGER_HOST: This variable needs to be present when deploying beyond local because if not, not even the basic acces tests wont work. This variable is used inside app/_ _ init _ _.py. This will select the correct host depending on the deployment type.

2. DATABASE_TYPE: This variable determines what set of variables your instance will get to connect to the database. It defaults to "sqlite". Docker compose sets it up to the db container.

3. FLASK_ENV: This allows the app to know what origins have to allow

4. RPI_MODULE: In this moment, setting up this variable loads RPI blueprint for control. Value? Whatever you want, its not used

## Testing
Execute this commands in the root folder.
If you have problems with importing modules, try:

    export PYTHONPATH=<absolute-path to folder>
    set PYTHONPATH=<absolute-path to folder>

To run the tests:

    pytest

If you want to generate lcov files:

    pytest --cov=. --cov-report=lcov

## Raspberry Pi

If you intend to use this backend in a raspberry pi to have pin acces is mandatory you run in standalone mode. This is because if you execute this inside docker, you will have to jump fire hoops to have pin access. Its better this way, because you can connect an archetype frontend in other ways.

It's important to set RPI_MODULE variable to any value to detect the need of pin control.

