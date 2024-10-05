# How to execute

## Standalone
    python run.py

## Docker compose
This is integral part of a full arquetype to develop apps. This dockerfile fits with a docker compose on a upper level.
On parent directory:
    
    docker compose up -d

## Reason of the separation
In order to deploy in Google Cloud Run we have to separate every image from every service.

This repository isolates the backend part and shows its workings in swagger. In this moment theres a instance working here:
https://back-arquetipo-856517455627.europe-southwest1.run.app/swagger

It lacks DB connection because we dont know if its advisable to spin a db container in this kind of setup.

# How to deploy to Cloud Run
1. Check if the container builds and runs locally.
2. Go to: https://console.cloud.google.com/run
3. Deploy container, service
4. Implement from Github
5. Configure Cloud Build (is mandatory)
6. Pick repositoriy/add permisions to read your repos.
7. Pick DOCKERFILE compilation.
8. Create service.

This will create the cloud build trigger and the cloud run function as service.