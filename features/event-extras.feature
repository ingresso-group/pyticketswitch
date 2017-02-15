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
                    "value": "Roseberry Avenue\r\nIslington\r\nLondon\r\nUK",
                    "value_html": "<p>Roseberry Avenue\r\nIslington\r\nLondon\r\nUK</p>"
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
                "value": "Roseberry Avenue\r\nIslington\r\nLondon\r\nUK",
                "value_html": "<div><p>Roseberry Avenue\r\nIslington\r\nLondon\r\nUK</p></div>\n"
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
                "url": "https://d1wx4w35ubmdix.cloudfront.net/shared/event_media/cropper/5e/5e004f25b5aab6f432cd7e6839b70942d8a5f17b.jpg",
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
        And the cost range min surcharge is "0.0"
        And the cost range max surcharge is "0.0"
