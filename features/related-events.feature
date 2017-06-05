Feature: related_events
    In order to show related events for sale to my customer
    As a Developer
    I need to retrieve the related events and addons for an event or trolley.

    Scenario: addon events with existing trolley
        Given an API client with valid credentials
        And I have an existing trolley with items from "7AB" in it
        When I fetch addon events for my trolley
        Then I get a list of addon events
        And the addon event list contains "7AC"

    Scenario: upsell events without a trolley
        Given an API client with valid credentials
        And my customer wants tickets to "7AB"
        When I fetch upsell events for the tickets
        Then I get a list of upsell events
        And the upsell event list does not contain "7AB"
        And the upsell event list contains "7AA"
