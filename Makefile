.PHONY: docs publish-docs

DOCS_TO_BRANCH=gh-pages
DOCS_FROM_BRANCH=master

init:
	virtualenv venv -p python3
	./venv/bin/pip install pip --upgrade
	./venv/bin/pip install -r requirements/test.txt
	./venv/bin/pip install -r requirements/docs.txt
	./venv/bin/pip install -e .

clean:
	rm -rf ./venv fixtures/cassettes *.egg-info .tox .cache .coverage
	find . -name "*.pyc" -exec rm -rf {} \;

test:
	flake8 pyticketswitch
	pylint pyticketswitch
	py.test
	behave

docs:
	cd docs && make html
	@echo "Build successful! View the docs homepage at docs/_build/html/index.html."

publish-docs: docs
	git checkout $(DOCS_TO_BRANCH)
	git reset $(DOCS_FROM_BRANCH) --hard
	find . -maxdepth 1  -not -name 'docs' -not -name '.git' -not -name 'venv' -not -name '.' | xargs rm -rf
	mv ./docs/_build/html/* .
	rm -rf docs
	echo 'venv' > .gitignore
	touch .nojekyll
	git add -A
	git commit -m 'updating documentation!'
	git push origin $(DOCS_TO_BRANCH) --force
	git checkout -

publish:
	pip install twine
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*
	rm -fr build dist .egg pyticketswitch.egg-info
