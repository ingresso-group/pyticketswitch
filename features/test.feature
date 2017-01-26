Feature: wrap the /f13/test.v1 endpoint
    In order to check credentials and the health of the remote API
    As a developer
    I want to be able to call a simple method and have it raise an exception
    if there is something wrong.

    Scenario: Valid credentials
        Given an API client with valid credentials
        When the test method is called
        Then the response should contain a User object

    Scenario: Invalid credentials
        Given an API client with invalid credentials
        When the test method is called
        Then an authorisation error should be raised
