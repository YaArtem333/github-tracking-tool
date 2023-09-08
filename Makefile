requirements: ## Install requirements
	pip install requests
	pip install flask
	pip install pymongo
	pip install bs4
	pip install lxml

run: requirements ## Run app
	python main.py

requirements_for_tests:
	pip install pytest
	pip install mongomock
	pip install pytest-cov

tests: requirements_for_tests## Run tests
	pytest -v tests

coverage: requirements_for_tests ## Run tests with coverage
	pytest --cov-report term --cov=app tests/