# Testing Strategy

## Unit tests

**Scope**: For testing library classes and methods. Tests use mocked HTTP responses.

**Framework**: pytest framework run via make test with code coverage

**Mocking**: requests-mock, mock

**Organization**: Tests in [tests/](../tests/) mirror source structure

**Coverage**: 35 test files covering all modules:
- [test_client.py](../tests/test_client.py) - Main client methods (75KB, most comprehensive)
- [test_event.py](../tests/test_event.py) - Event parsing and models
- [test_availability.py](../tests/test_availability.py) - Availability responses
- [test_order.py](../tests/test_order.py) - Order processing
- [test_performance.py](../tests/test_performance.py) - Performance data
- [test_trolley.py](../tests/test_trolley.py) - Shopping cart functionality

## Integration Tests

**Scope**: For testing end-to-end API interactions. Tests use VCRpy cassettes to record/replay HTTP responses.

**Framework**: behave framework run via make test

**Organization**: Gherkin scenarios in [features/](../features/) covering API operations

**Coverage**: 51 scenarios across 16 feature files:
- [event-extras.feature](../features/event-extras.feature) - Event extras (8 scenarios)
- [purchase.feature](../features/purchase.feature) - Purchase flows (7 scenarios)
- [reserve.feature](../features/reserve.feature) - Reservation flows (6 scenarios)
- [search-events.feature](../features/search-events.feature) - Event search (6 scenarios)
- [trolley.feature](../features/trolley.feature) - Trolley operations (6 scenarios)
- [availability.feature](../features/availability.feature) - Availability queries (3 scenarios)
- [list-performances.feature](../features/list-performances.feature) - Performance listing (3 scenarios)
- [get-events.feature](../features/get-events.feature) - Event retrieval (2 scenarios)
- [get-performance.feature](../features/get-performance.feature) - Performance retrieval (2 scenarios)
- [related-events.feature](../features/related-events.feature) - Related events (2 scenarios)
- [test.feature](../features/test.feature) - API connection test (2 scenarios)
- [get-purchase.feature](../features/get-purchase.feature) - Purchase retrieval (1 scenario)
- [get-reservation.feature](../features/get-reservation.feature) - Reservation retrieval (1 scenario)
- [release.feature](../features/release.feature) - Release operations (1 scenario)
- [status.feature](../features/status.feature) - Status queries (1 scenario)

**VCR Cassettes**: HTTP responses recorded via VCRpy for reproducible tests

## Commands

```bash
make test     # all (flake8 + pylint + pytest + behave + coverage)
make flake    # flake8 only
tox           # run tests across Python versions
```

## CI Integration

CircleCI runs on every push ([.circleci/config.yml](../.circleci/config.yml)):
1. flake8 - Style checks
2. black - Code formatting
3. behave coverage - Integration tests with coverage
4. pytest coverage - Unit tests with coverage
5. Coverage report to Codecov
