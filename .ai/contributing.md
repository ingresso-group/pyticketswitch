# Contributing

## Local Setup

**First time setup**:

1. **Python**: make init (from [Makefile](../Makefile)) which does:
   - Create virtualenv: virtualenv venv -p python3
   - Update package manager: pip install pip --upgrade
   - Install test requirements: pip install -r requirements/test.txt
   - Install docs requirements: pip install -r requirements/docs.txt
   - Install package in editable mode: pip install -e .

**Alternative setup with tox**:

1. **Tox**: pip install tox
2. **Run**: tox (runs tests across Python versions)

## Local Run

- **Activate venv**: source venv/bin/activate
- **Install package**: pip install -e .
- **Use in Python**: from pyticketswitch import Client

## Workflow

**Branching**:

- **Main branch**: `master` containing production ready code
- **Feature branches**: Fork and create feature branches

**Commits**:

- Bug fixes should have a unit test that ensures the bug is never reintroduced
- New features should have an acceptance test
- All tests (both new and old) should be passing

**Testing**:

1. **Style checks**: flake8 pyticketswitch
2. **Unit tests**: py.test
3. **Integration tests**: behave

All tests should pass before merging and can be run using make test command.

## Versioning

- [Semantic Versioning](https://semver.org/)
- Version defined in [setup.py](../setup.py) and [pyticketswitch/__init__.py](../pyticketswitch/__init__.py)
- Changelog maintained in [CHANGELOG.md](../CHANGELOG.md)

## Documentation

- [Pyticketswitch Documentation](https://pyticketswitch.ingresso.co.uk)
- [F13 API Documentation](https://docs.ingresso.co.uk/)
- Built with Sphinx in [docs/](../docs/)
