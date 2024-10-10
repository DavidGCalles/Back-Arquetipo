## Historic Knowledge
Initially this project was one big archetype but wanting to be used on cloud run deployments we had to split it up to be more versatile.

This repository isolates the backend part of that project and aims to be a solid backbone to deploy any API needed on cloud run and another serverless services. We have an archetype working right here:
https://back-arquetipo-856517455627.europe-southwest1.run.app/swagger

# How to execute

## Standalone
    python run.py

# How to deploy with docker
1. docker run -d -p 5000:5000 your-image-name
2. http://localhost:5000/swagger

# Known issues
- It lacks DB connection in Cloud Run because we dont know if its advisable to spin a db container in this kind of setup.

# How to deploy to Cloud Run

## Prerequisites
1. Check if the container builds and runs locally. This step is very important, because you can avoid a lot of headaches knowing for sure your build runs.

## Cloud Run

1. Go to: https://console.cloud.google.com/run
1. Select your project.
1. Click on deploy container and then service, service [insertar imagen deploycontainer.png]
1. Implement from Github [selectgithub.png]

### Core Configuration
1. Configure minimal Cloud Build (is mandatory)[setupcloudbuild]
    1. Connect your github if its not connected.
    1. Select the repository (the fork of the arquetype on which the app is developed)
    1. Push Next. Select Dockerfile build type
1. Configure name and region (important on pricing and time response)[configureService.png]
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