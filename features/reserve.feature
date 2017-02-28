Feature: reserve tickets
    In order to make sure no one else purchases the tickets my user is 
    interested in while they enter their payment details.
    As a Developer
    I want to be able to reserve the tickets for a short amount of time.

    @dirty
    Scenario: best available event
        Given an API client with valid credentials
        And my customer wants tickets to "6IF"
        When I reserve the tickets
        Then my reservation is successful

    @wip
    @dirty
    Scenario: best available event with discounts
        Given an API client with valid credentials
        And my customer wants tickets to "6IF"
        And my customer has requested some discounts
        When I reserve the tickets
        Then my reservation is successful
        And my reservation has some discounts

    @wip
    @dirty
    Scenario: best available event with non default send method
        Given an API client with valid credentials
        And my customer wants tickets to "6IF"
        And my customer wants them posted to them
        When I reserve the tickets
        Then my reservation is successful
        And my send method is the one I requested

    @wip
    @dirty
    Scenario: seated event with seats
        Given an API client with valid credentials
        And my customer wants tickets to "3CVF"
        And my customer is requesting specific seats
        When I reserve the tickets
        Then my reservation is successful
        And I get the requested seats

    @wip
    @dirty
    Scenario: seated event with unavailable seats
        Given an API client with valid credentials
        And my customer wants tickets to "3CVF"
        And my customer is requesting unavailable specific seats
        When I reserve the tickets
        Then my reservation is successful
        And I get different seats than requested
