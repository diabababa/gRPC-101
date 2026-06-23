Feature: Chat Service — Gherkin Practice (Solution)

  Scenario: Send a message successfully
    Given the Chat service is running
    When I send a message to room "gherkin-demo" as user "workshop" with content "Hello Gherkin!"
    Then I receive a response with a non-empty message_id
    And the response status is "ok"

  Scenario: Empty content is rejected
    Given the Chat service is running
    When I send a message with empty content
    Then the service returns status code INVALID_ARGUMENT

  Scenario: Retrieve chat history after sending messages
    Given the Chat service is running
    And 3 messages were sent to room "gherkin-history"
    When I request history for room "gherkin-history" with limit 10
    Then I receive a stream of 3 messages

  Scenario: Bulk send reports correct count
    Given the Chat service is running
    When I stream 5 messages to room "gherkin-bulk"
    Then the service reports 5 messages sent
