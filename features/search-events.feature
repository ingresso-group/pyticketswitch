Feature: search for events
    In order to display a list of events to a user
    As a developer
    I want to be able to call a method with some search parameters and recieve
    a list of filtered and paginated events

    Scenario: keyword search
        Given an API client with valid credentials
        When a search for "nutcracker, sadlers" keywords is performed
        Then a single event should be returned
        And that event should have the ID of "6IF"

    Scenario: date range search
        Given an API client with valid credentials
        When a search for events with performances "30"-"37" days from now is performed
        Then the events all have a performance between "30" and "37" days from now

    Scenario: country search
        Given an API client with valid credentials
        When a search for events in country with code "jp" is performed
        Then all events are in country with code "jp"

    Scenario: city search
        Given an API client with valid credentials
        When a search for events in city with code "paris-fr" is performed
        Then all events are in city with code "paris-fr"

    Scenario: geo search
        Given an API client with valid credentials
        When a search for events within "100"km of "35.5000" lat and "139.300" long is performed
        Then the events are all within "100"km of "35.5000" lat and "139.300" long

    Scenario: paginated search
        Given an API client with valid credentials
        When a search is performed for page 2 with a page length of 3 is performed
        Then the 7, 8 and 9th events are returned
