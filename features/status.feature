Feature: get the transaction/reservation status
    In order to display the current state of a transaction/reservation to a
    customer
    As a Developer
    I want to be able retrieve the state of the transaction

    Scenario: get a completed transaction
        Given I have a completed transaction
        When I fetch the status of the transaction
        Then the status is "purchased"
