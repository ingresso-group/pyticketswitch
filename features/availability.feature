Feature: availability
    In order to display ticket for sale to my customer
    As a Developer
    I need to retrieve the available tickets and prices for a performance.

    Scenario: seated performance
        Given an API client with valid credentials
        And I have a performance ID for event with ID "6IE"
        When I fetch availabilty for my performance
        Then I get a list of available ticket types
        And each ticket type has at least one price band
        And each price band has a price
        And each price band has some example seats

    Scenario: seated performance with seat selection
        Given an API client with valid credentials
        And I have a performance ID for event with ID "7AB"
        When I fetch availabilty for my performance
        Then I get a list of available ticket types
        And each ticket type has at least one price band
        And each price band has a price
        And each price band has some real seats

    Scenario: non seated performance
        Given an API client with valid credentials
        And I have a performance ID for event with ID "AG8"
        When I fetch availabilty for my performance
        Then I get a list of available ticket types
        And each ticket type has at least one price band
        And each price band has a price
