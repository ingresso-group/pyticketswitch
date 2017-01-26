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
        When a search for events with performances "700"-"710" days from now
        Then a list of "5" events should be returned
        And those events should have the ID's "6KS, 6KT, GVA, 3CVG, 3CVE"

    Scenario: country search
        Given an API client with valid credentials
        When a search for events in country with code "jp"
        Then a single event should be returned
        And that event should have the ID of "AG8"

    Scenario: city search
        Given an API client with valid credentials
        When a search for events in city with code "belfast-uk"
        Then a single event should be returned
        And that event should have the ID of "2HJD"

    Scenario: geo search
        Given an API client with valid credentials
        When a search for events withing "5"km of "51.491188" lat and "-0.223731" long
        Then a list of "4" events should be returned
        And those events should have the ID's "I3U, 6KF, I3T, 3S0L"
