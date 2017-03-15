Feature: fiddle with the transport layer
    In order to control how my application talks to the API
    As a Developer
    I want to be able to access the internals of the requests library

    @wip
    Scenario: adjust timeouts
        Given that some API calls take over 10 seconds to complete
        And I override the client to timeout after 2 seconds
        When I make a call
        Then after 2 seconds a timeout exception is raised.

    @wip
    Scenario: retries
        Given that some API calls fail due to networking issues
        And I override the client to retry until I get a response
        When I make the call
        Then I eventually get a response
