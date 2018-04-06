Feature: add additional information to request
    In order to get additional information about an event
    As a developer
    I want to provide addtional arguments to methods that return and event
    and have the response extended.

    Scenario: get single event with availability
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting availability
        Then a single event should be returned
        And the event has availability details

    Scenario: get single event with availability and performance information
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting availability with performances
        Then a single event should be returned
        And the event has availability details
        And the availability details have performance information

    Scenario: get single event with extra info
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting extra info
        Then a single event should be returned
        And the event has content information
            """
            {
                "address": {
                    "value": "Roseberry Avenue Islington London UK\n",
                    "value_html": "<p>Roseberry Avenue Islington London UK</p>"
                }
            }
            """
        And the event has event information starting with
            """
            {
                "value": "Matthew Bourne's stunning production",
                "value_html": "<div><p>Matthew Bourne's stunning production "
            }
            """
        And the event has venue information
            """
            {
                "value": "Roseberry Avenue Islington London UK\n",
                "value_html": "<p>Roseberry Avenue Islington London UK</p>"
            }
            """

    Scenario: get single event with reviews
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting reviews
        Then a single event should be returned
        And the event has "2" reviews

    Scenario: get single event with media
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting media
        Then a single event should be returned
        And the event has media
        """
        {
            "square": {
                "caption": "",
                "caption_html": "",
                "name": "square",
                "url": "https://d1wx4w35ubmdix.cloudfront.net/media/event/6IF/matthew-bournes-nutcracker-test-square-Z0Jk.jpg?versionId=09daZJn.14RH7.84cRKXK2FfODDmFYpC",
                "secure": true,
                "width": null,
                "height": null
            },
            "video": {
                "caption": "",
                "caption_html": "",
                "name": "video",
                "url": "https://www.youtube.com/embed/G1JpEHGizk4?rel=0",
                "secure": true,
                "width": 420,
                "height": 315
            }
        }
        """

    Scenario: get single event with cost range
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "6IF" requesting cost ranges
        Then a single event should be returned
        And the event has cost range
        And the cost range min seatprice is "18.0"
        And the cost range max seatprice is "47.0"
        And the cost range min surcharge is "3.0"
        And the cost range max surcharge is "5.0"

    Scenario: get single event with add-ons
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "7AB" with add-ons
        Then a single event should be returned
        And the event has add-ons
        And the add-ons contain "7AC"

    Scenario: get single event with upsells
        Given an API client with valid credentials
        When we attempt to fetch events with the ID's "7AB" with upsells
        Then a single event should be returned
        And the event has upsells
        And the upsells contain "7AA"
        And the upsells do not contain "7AB"
