Feature: Get a reservation
    In order to find out information about a purchase quickly
    As a Developer
    I want to be able to quickly retrieve a copy of the original purchase response

    Scenario: Get a previously made purchase
        Given I have already purchased tickets
        When I get the purchase
        Then the purchase response is the same as the original
