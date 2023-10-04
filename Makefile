LINT_PATHS = .

include .env.dev

lint:
	isort $(LINT_PATHS) --diff --check-only
	pylint $(LINT_PATHS)
	mypy $(LINT_PATHS) --install-types --non-interactive

format:
	isort $(LINT_PATHS)
	black $(LINT_PATHS)

test:
	@echo "Running tests..."
	pytest --cov -s --cov-report xml:.coverage.xml

runserver:
	@echo 'Running spotideets development server...'
	python -X dev manage.py runserver

resetdbmigrations:
	@echo 'Deleting database and flushing migrations'
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
	dropdb spotideets
	createdb spotideets
	python manage.py makemigrations
	python manage.py migrate

%:
	@:
