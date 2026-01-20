# Code Standards

**Style**

- Python 2.7/3.x compatible (uses six for compatibility)
- Python conventions ([PEP 8](https://www.python.org/dev/peps/pep-0008/))
- Flake8 linter ([setup.cfg](../setup.cfg)) - max-complexity=15, max-line-length=137
- Black formatter for consistent code style
- Pylint for additional code quality checks

**Naming conventions**:

- One class per module: [event.py](../pyticketswitch/event.py) → Event, [performance.py](../pyticketswitch/performance.py) → Performance
- CamelCase for class names
- snake_case for functions/variables/modules
- UPPER_CASE for constants

**Language patterns**:

- Factory methods (from_api_data() class methods)
- Mixins for shared behavior ([mixins.py](../pyticketswitch/mixins.py))
- Comprehensive docstrings with Args/Returns/Raises
- Property decorators for computed attributes

## File Organization

**Codebase**:

- Library code: [pyticketswitch/](../pyticketswitch/) (39 modules)
  - Main client: [client.py](../pyticketswitch/client.py)
  - Exceptions: [exceptions.py](../pyticketswitch/exceptions.py)
  - Utilities: [utils.py](../pyticketswitch/utils.py)

- Package setup: [setup.py](../setup.py)

**Tests**

- Unit tests: [tests/](../tests/)
- Integration tests: [features/](../features/)

**CI/CD**:

- Pipeline: [.circleci/config.yml](../.circleci/config.yml)
- Commands: [Makefile](../Makefile)

**Configuration**:

- Style: [setup.cfg](../setup.cfg)
- Tox: [tox.ini](../tox.ini)
- Behave: [behave.ini](../behave.ini)

## Dependencies

- Python packages: [requirements/common.txt](../requirements/common.txt)
- Test packages: [requirements/test.txt](../requirements/test.txt)
- Docs packages: [requirements/docs.txt](../requirements/docs.txt)
