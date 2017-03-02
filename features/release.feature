Feature: release a reservation
    In order for another customer to be able to purchase the tickets I have reserved
    As a Developer
    I want to be able to release my reservation.

    @wip
    Scenario: release a reservation
        Given an API client with valid credentials
        And an event with availability
        And I have reserved tickets for my customer for this event
        When I release the reservation
        Then the reservation is successfully released
