Feature: add tickets to the trolley
    In order for my customer to purchase multiple products
    As a Developer
    I want to be able to add items to a trolley.

    Scenario: create a trolley
        Given an API client with valid credentials
        And my customer wants tickets to "6IF"
        When I add the tickets to the trolley
        Then I get a trolley token
        And my trolley contains tickets for "6IF"

    Scenario: create a trolley with discounts
        Given an API client with valid credentials
        And my customer wants tickets to "6IF"
        And my customer has requested some discounts
        When I add the tickets to the trolley
        Then I get a trolley token
        And my trolley contains tickets for "6IF"
        And my trolley has some discounts

    Scenario: create a trolley with seats
        Given an API client with valid credentials
        And my customer wants tickets to "7AB"
        And my customer is requesting specific seats
        When I add the tickets to the trolley
        Then I get a trolley token
        And my trolley contains the requested seats

    Scenario: add item to an existing trolley
        Given an API client with valid credentials
        And I have an existing trolley with items from "6IF" in it
        And my customer wants tickets to "6IE"
        When I add the tickets to the trolley
        Then I get a trolley token
        And my trolley contains tickets for "6IF"
        And my trolley contains tickets for "6IE"

    Scenario: remove item from an existing trolley
        Given an API client with valid credentials
        And I have an existing trolley with items from "6IF" in it
        And I have an existing trolley with items from "6IE" in it
        When I remove some tickets for "6IE" from the trolley
        Then I get a trolley token
        And my trolley contains tickets for "6IF"
        And my trolley does not contain tickets for "6IE"
