.PHONY: makemigrations
makemigrations:
	docker-compose run --rm web python manage.py makemigrations


.PHONY: migrate
migrate:
	docker-compose run --rm web ./docker/wait-for-postgres.sh "poetry run python manage.py migrate"


.PHONY: dshell
dshell:
	docker-compose run --rm web python manage.py shell


.PHONY: psql
psql:
	docker-compose run --rm postgres psql --host=postgres --dbname=postgres --username=postgres
