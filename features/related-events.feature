Feature: related_events
    In order to show related events for sale to my customer
    As a Developer
    I need to retrieve the related events and addons for an event or trolley.

    Scenario: upsell events with existing trolley
        Given an API client with valid credentials
        And I have an existing trolley with items from "7AB" in it
        When I fetch related events for my trolley
        Then I get a list of upsell events
        And the upsell event list does not contain "7AB"
        And the upsell event list contains "7AA"

    Scenario: upsell events with a list of event IDs
        Given an API client with valid credentials
        When I fetch related events for the list of event IDs "7AB"
        Then I get a list of upsell events
        And the upsell event list does not contain "7AB"
        And the upsell event list contains "7AA"
