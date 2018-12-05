Feature: Get a reservation
    In order to find out information about a reservation quickly
    As a Developer
    I want to be able to quickly retrieve a copy of the original reservation response

    @dirty
    Scenario: Get a previously made reservation
        Given an API client with valid credentials
        And an event with availability
        And I have reserved tickets for my customer for this event
        When I get the reservation
        Then the reservation response is the same as the original
