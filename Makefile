.PHONY: docs publish-docs

init:
	virtualenv venv -p python3
	./venv/bin/pip install pip --upgrade
	./venv/bin/pip install -r requirements/test.txt
	./venv/bin/pip install -r requirements/docs.txt
	./venv/bin/pip install -e .

clean:
	rm -rf ./venv fixtures/cassettes *.egg-info .tox .cache .coverage
	find . -name "*.pyc" -exec rm -rf {} \;

flake:
	flake8 pyticketswitch

test:
	flake8 pyticketswitch
	pylint pyticketswitch
	coverage run -m pytest tests
	coverage run -m behave --no-capture --no-color --format progress2 --junit --tags=-skip
	coverage combine
	coverage report --show-missing

docs:
	cd docs && make html
	@echo "Build successful! View the docs homepage at docs/_build/html/index.html."

publish:
	pip install twine wheel
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	rm -fr build dist .egg pyticketswitch.egg-info
