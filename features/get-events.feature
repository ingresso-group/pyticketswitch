Feature: get specific events
    In order to display information about a specific event or set of events
    As a developer
    I want to be able retrieve information specific to a given event or set of
    events with out repeating a search

    Scenario: single event
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF"
        Then those events should have the ID's "6IF"
