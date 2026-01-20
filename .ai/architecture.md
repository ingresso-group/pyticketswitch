# Architecture

## Overview

Python SDK/library providing a wrapper for the Ingresso F13 API. Enables event search, availability checking, reservations, and ticket purchases. Synchronous HTTP client using the requests library.

**API Documentation**: [Ingresso F13 API](https://docs.ingresso.co.uk/)

## Stack

- Python 2.7/3.x, requests, python-dateutil, six
- Synchronous HTTP with requests library
- JSON response parsing with decimal support

## Structure

**Codebase**:

- Library code: [pyticketswitch/](../pyticketswitch/) (39 modules)
  - Main client: [client.py](../pyticketswitch/client.py)
  - Exceptions: [exceptions.py](../pyticketswitch/exceptions.py)
  - Utilities: [utils.py](../pyticketswitch/utils.py)
  - Core models: [event.py](../pyticketswitch/event.py), [performance.py](../pyticketswitch/performance.py), [reservation.py](../pyticketswitch/reservation.py), [status.py](../pyticketswitch/status.py)

- Package setup: [setup.py](../setup.py)

**Dependencies**:

- Python packages: [requirements/common.txt](../requirements/common.txt)
- Test packages: [requirements/test.txt](../requirements/test.txt)
- Docs packages: [requirements/docs.txt](../requirements/docs.txt)

**Tests**

- Unit tests: [tests/](../tests/) (35 test files)
- Integration tests: [features/](../features/) (16 feature files, 51 scenarios)

**CI/CD**:

- Pipeline: [.circleci/config.yml](../.circleci/config.yml)
- Commands: [Makefile](../Makefile)

**Configuration**:

- Style: [setup.cfg](../setup.cfg)
- Tox: [tox.ini](../tox.ini)
- Behave: [behave.ini](../behave.ini)

## Build & Deploy

**Local**:

- Virtualenv build using make init from [Makefile](../Makefile)
- Run with pip install -e .

**PyPI**:

- Published to PyPI as pyticketswitch package
- Install with pip install pyticketswitch
- Publish with make publish from [Makefile](../Makefile)

## Configuration

- API credentials passed to Client constructor (user, password)
- Optional: sub_user, language, tracking_id, use_decimal
- Default API URL: https://api.ticketswitch.com
