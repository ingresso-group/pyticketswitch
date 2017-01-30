Feature: add additional information to request
    In order to get additional information about an event
    As a developer
    I want to provide addtional arguments to methods that return and event
    and have the response extended.


    Scenario: search with availability
        Given an API client with valid credentials
        When a search for "nutcracker, sadlers" keywords requesting availability is performed  
        Then a single event should be returned
        And the event has availability details

    Scenario: get single event with availability
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting availability
        Then a single event should be returned
        And the event has availability details

    Scenario: search with availability and performance information
        Given an API client with valid credentials
        When a search for "nutcracker, sadlers" keywords requesting availability with performances is performed  
        Then a single event should be returned
        And the event has availability details
        And the availability details have performance information

    Scenario: get single event with availability and performance information
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting availability with performances
        Then a single event should be returned
        And the event has availability details
        And the availability details have performance information
