Feature: purchase tickets
    As a developer
    In order for my customers to buy the tickets they have reserved
    I want to be able to provide the users payment info, and receive 
    confirmation that the tickets are now booked

    Scenario: credit debitor
        Given my account is set up to allow a user to buy on credit
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        When I purchase the tickets
        Then the purchase is succesful

    Scenario: invalid customer details
        Given my account is set up to allow a user to buy on credit
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided invalid customer information
        When I purchase the tickets
        Then I get an error indicating that the customer details are incorrect

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

    Scenario: invalid card details
        Given my account is set up to use a card debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And my user has provided invalid credit card details
        When I purchase the tickets
        Then I get an error indicating that the card details are incorrect

    @dirty
    Scenario: redirect debitor part one
        Given my account is set up to use a redirect debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And I provide a URL and token to return to
        When I purchase the tickets
        Then I get a callout

    @dirty
    Scenario: redirect debitor part two
        Given my account is set up to use a redirect debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And I provide a URL and token to return to
        And I have returned from a successful external payment
        When I ask for the next redirect
        Then the purchase is succesful
        And I get a ticketswitch booking reference
        And I get a booking reference from the backend system

    @dirty
    Scenario: redirect fails
        Given my account is set up to use a redirect debitor
        And an event with availability
        And I have reserved tickets for my customer for this event
        And my user has provided valid customer information
        And I provide a URL and token to return to
        And I have returned from a failed external payment
        When I ask for the next redirect
        Then the purchase fails
