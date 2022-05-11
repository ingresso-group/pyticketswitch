Feature: list performances
    In order to display to a user what dates are available for an event
    As a developer
    I want to be able retrieve a performance information.

    Scenario: event with a set of chronological performances
        Given an API client with valid credentials
        When I fetch performances for the event "6IF"
        Then I get a list of performances

    Scenario: event with named performances
        Given an API client with valid credentials
        When I fetch performances for the event "DP9"
        Then I get a list of performances
        And I get an indication that the performances have names

    Scenario: event with an auto selected performance
        Given an API client with valid credentials
        When I fetch performances for the event "6KS"
        Then I get one performance
        And I get an indication that the performance is auto selected
