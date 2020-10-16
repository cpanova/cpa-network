.PHONY: makemigrations
makemigrations:
	docker-compose run --rm web python manage.py makemigrations


.PHONY: migrate
migrate:
	docker-compose run --rm web python manage.py migrate


.PHONY: dshell
dshell:
	docker-compose run --rm web python manage.py shell


.PHONY: flake
flake:
	docker-compose run --rm web flake8 . | grep -v migrations | grep -v 'dao.py'


.PHONY: pytest
pytest:
	docker-compose run --rm web pytest


.PHONY: test
test:
	docker-compose run --rm web python manage.py test


.PHONY: mypy
mypy:
	docker-compose run --rm web mypy .


.PHONY: psql
psql:
	docker-compose run --rm postgres psql --host=postgres --dbname=postgres --username=postgres
