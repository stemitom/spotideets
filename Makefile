LINT_PATHS = spotideets/ manage.py

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

%:
	@: