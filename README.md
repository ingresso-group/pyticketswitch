Pyticketswitch
==============

Python wrapper for the ticketswitch [f13 API](http://ingresso-group.github.io/slate).

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

- Issue Tracker: github.com/ingresso-group/pyticketswitch/issues
- Source Code: github.com/ingresso-group/pyticketswitch
- F13 API Documentation: http://ingresso-group.github.io/slate

### Running tests ###

Tests can be run with [tox](https://pypi.python.org/pypi/tox):

```
pip install tox
tox
```

or manually:

```
pip install -r requirements/test.txt
flake8 pyticketswitch
py.test
behave
```

[Behave](http://pythonhosted.org/behave/) tests require 
[PyVCR](https://github.com/kevin1024/vcrpy). There are intentionally no
cassettes shipped with the repo (to avoid an echo chamber), so the first run
might be slow, but subsequent runs will be faster. Be mindful of this fake
though.

### Building Documentation ###

Documentation is generated with Syphinx


Support
-------

If you are having issues, let us know systems@ingresso.co.uk

License
-------

Copyright (c) 2016 Ingresso Group

Licensed under the The MIT License.
