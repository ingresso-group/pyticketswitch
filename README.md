Pyticketswitch
==============


[![Build Status](https://travis-ci.org/ingresso-group/pyticketswitch.svg?branch=master)](https://travis-ci.org/ingresso-group/pyticketswitch)
[![codecov](https://codecov.io/gh/ingresso-group/pyticketswitch/branch/master/graph/badge.svg)](https://codecov.io/gh/ingresso-group/pyticketswitch)
[![PyPI](https://img.shields.io/pypi/v/pyticketswitch.svg)](https://pypi.python.org/pypi/pyticketswitch)
[![PyPI](https://img.shields.io/pypi/pyversions/pyticketswitch.svg)](https://pypi.python.org/pypi/pyticketswitch)


Python wrapper for the ticketswitch [f13 API](https://docs.ingresso.co.uk/).

**Docs**: https://pyticketswitch.ingresso.co.uk
**F13 API Documentation**: https://docs.ingresso.co.uk/

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

License
-------

Copyright (c) 2017 Ingresso Group

Licensed under the The MIT License.
