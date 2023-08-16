.PHONY: lint
lint:
	flake8 .
	mypy .

.PHONY: po
po:
	python backend/manage.py makemessages --no-wrap --locale=en --locale=ru -i=*env

.PHONY: mo
mo:
	python backend/manage.py compilemessages --locale=en --locale=ru -i=*env

.PHONY: mm
mm:
	python backend/manage.py makemigrations

.PHONY: mg
mg:
	python backend/manage.py migrate

.PHONY: csu
csu:
	python backend/manage.py createsuperuser

.PHONY: run
run:
	python backend/manage.py runserver

.PHONY: cs
cs:
	python backend/manage.py collectstatic
