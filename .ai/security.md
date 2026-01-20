# Security

## Vulnerability Reporting

- Issue Tracker: https://github.com/ingresso-group/pyticketswitch/issues
- No formal security disclosure policy currently

## Secure Patterns

- No hardcoded credentials - auth passed via Client constructor
- HTTPS-only API communication (DEFAULT_ROOT_URL in [client.py](../pyticketswitch/client.py))
- Dependency pinning in [requirements/common.txt](../requirements/common.txt)
- Basic auth over HTTPS for API authentication

## Authentication

- API auth via Client constructor (user, password)
- Credentials encoded as UTF-8 and passed via HTTP Basic Auth
- Optional sub_user for agent identification
- Optional tracking_id for session tracking

## Common Pitfalls

- Exposing API credentials in code or version control
- Not using HTTPS (library enforces HTTPS by default)
- Storing credentials in plaintext configuration files
- Missing dependency updates for security patches
