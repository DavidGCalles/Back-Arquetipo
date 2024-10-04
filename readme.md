# How to execute

## Standalone
    python run.py

## Docker compose
This is integral part of a full arquetype to develop apps. This dockerfile fits with a docker compose on a upper level.
On parent directory:
    
    docker compose up -d

## Reason of the separation
In order to deploy in Google Cloud Run we have to separate every image from every service.