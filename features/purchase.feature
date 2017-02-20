Feature: purchase tickets
    As a developer
    In order for my customers to buy the tickets they have reserved
    I want to be able to provide the users payment info, and receive 
    confirmation that the tickets are now booked

    Scenario: card debitor
        Given my account is set up to use a card debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And my user has provided valid credit card details
        When I purchase the tickets
        Then the purchase is succesful
        And I get a ticketswitch booking reference
        And I get a booking reference from the backend system

    Scenario: invalid customer details
        Given my account is set up to use a card debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided invalid customer information
        And my user has provided valid credit card details
        When I purchase the tickets
        Then the purchase fails
        And I get an error indicating that the customer details are incorrect

    Scenario: invalid card details
        Given my account is set up to use a card debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And my user has provided invalid credit card details
        When I purchase the tickets
        Then the purchase fails
        Then I get an error indicating that the card details are incorrect

    @wip
    Scenario: redirect debitor (part one)
        Given my account is set up to use a redirect debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And I provide a URL and token to return to
        When I purchase the tickets
        Then I get a URL to redirect to

    @wip
    Scenario: redirect debitor (part two)
        Given an event with a redirect debitor
        And I have reserved tickets for my customer for this event
        And I have successfully completed the first part of the redirect purchase
        When I purchase the tickets
        Then I get a ticketswitch booking reference
        And I get a booking reference from the backend system

    @wip
    Scenario: redirect fails
        Given an event with a redirect debitor
        And I have reserved tickets for my customer for this event
        And I have failed to completed the first part of the redirect purchase
        When I purchase the tickets
        Then I get an error indicating that the purchase has failed