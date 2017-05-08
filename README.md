Pyticketswitch
==============

Python wrapper for the ticketswitch [f13 API](http://ingresso-group.github.io/slate).

Docs: https://ingresso-group.github.io/pyticketswitch

Features
--------

- Search for events and performances.
- Availability details for performances.
- Make live reservations.
- Purchase tickets.

Installation
------------

Install pyticketswitch by running:

```
pip install pyticketswitch
```

Contribute
----------

- Issue Tracker: https://github.com/ingresso-group/pyticketswitch/issues
- Source Code: https://github.com/ingresso-group/pyticketswitch
- F13 API Documentation: https://ingresso-group.github.io/slate

### How to contribute ###

1. Check for open/closed issues.
2. Open a new issue describing the bug/feature.
3. Fork the repository
4. Bug fixes should have a unit test that ensures that the bug is never
   reintroduced. New features should have an acceptance test. All tests (both
   new and old) should be passing
5. Send us a pull request.

### Running tests ###

Tests can be run with [tox](https://pypi.python.org/pypi/tox):

```
pip install tox
tox
```

Or manually:

```
pip install -r requirements/test.txt
flake8 pyticketswitch
py.test
behave
```

Or via make

```
make test
```

[Behave](http://pythonhosted.org/behave/) tests require 
[PyVCR](https://github.com/kevin1024/vcrpy). There are intentionally no
cassettes shipped with the repo (to avoid an echo chamber), so the first run
might be slow, but subsequent runs will be faster. Be mindful of this fake
though.


### Documentation ###
Documentation is generated with [Syphinx](http://www.sphinx-doc.org/en/stable/)
and can be triggered from the make file:

```
make docs
```

In-line documentation follows 
[the google format](http://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html).


License
-------

Copyright (c) 2016 Ingresso Group

Licensed under the The MIT License.
