Feature: list the orders sold
    In order to report on what my user has sold
    As a developer
    I want to be able to list the orders that were sold through my user

    Scenario: find the order for a completed transaction
        Given I have a completed transaction
        When I list the orders sold for the transaction
        Then I get one order
        And the order is for the transaction
        And the order was purchased successfully

    Scenario: page through the orders sold
        Given an API client with valid credentials
        And my user has sold at least two orders
        When I list the orders sold one at a time for the first two pages
        Then each page has one order
        And the two pages have different orders

    Scenario: only list orders purchased after a time
        Given an API client with valid credentials
        When I list the orders sold that were purchased from tomorrow
        Then I get no orders

    Scenario: excluding purchased orders without including failed ones
        Given an API client with valid credentials
        When I list the orders sold excluding purchased orders but not including failed ones
        Then an invalid parameters error is raised
