#!/bin/bash

# Run the following to initialize GCP (only need to once)
gcloud auth login
gcloud auth configure-docker us-east1-docker.pkg.dev
gcloud config set run/region us-east1

# Run the following to setup your docker image
docker compose build
docker tag app_web us-east1-docker.pkg.dev/certain-ellipse-392102/django-web/web
# Run the following to push the docker image to the GCP repo
docker push us-east1-docker.pkg.dev/certain-ellipse-392102/django-web/web
# Run the following to start the server
gcloud run deploy django-test-web --image us-east1-docker.pkg.dev/certain-ellipse-392102/django-web/web --port 8000 --allow-unauthenticated