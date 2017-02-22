.PHONY: docs

init:
	virtualenv venv
	./venv/bin/pip install pip --upgrade
	./venv/bin/pip install -r requirements/test.txt
	./venv/bin/pip install -r requirements/docs.txt
	./venv/bin/pip install -e .

clean:
	rm -rf ./venv fixtures/cassettes *.egg-info .tox .cache .coverage
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	flake8 pyticketswitch
	py.test
	behave

publish:
	pip install twine
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	rm -fr build dist .egg pyticketswitch.egg-info

docs:
	cd docs && make html
	@echo "Build successful! View the docs homepage at docs/_build/html/index.html."
