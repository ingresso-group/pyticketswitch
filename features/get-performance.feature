Feature: get performances
    In order to display information on a specific performance
    As a developer
    I want to retrieve a specific performance using it's ID.

    Background:
        Given an API client with valid credentials
        Given I have a list of performances for event with id "6IF" 

    Scenario: single performance
        When I fetch a specific performance
        Then I get the performance

    Scenario: mutliple performances
        When I fetch multiple performances
        Then I get the performances
