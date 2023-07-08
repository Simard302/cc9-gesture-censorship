.PHONY: build
build:
    docker-compose run --rm web sh -c "python3 manage.py collectstatic"

.PHONY: deploy
deploy: build
    docker-compose -f docker-compose-deploy.yml run --rm gcloud sh -c "gcloud app deploy --project certain-ellipse-392102"