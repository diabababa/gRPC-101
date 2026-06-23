Feature: First gRPC Service — Unary RPC

  Scenario: Send a message and receive confirmation
    Given the Chat service is running
    When I send a message to room "general" as user "alice" with content "Hello EuroPython!"
    Then I receive a response with a non-empty message_id
    And the response status is "ok"
    And the response has a positive timestamp

  Scenario: Message IDs are unique for each request
    Given the Chat service is running
    When I send two messages to room "unique-test"
    Then each message has a different message_id

  Scenario: Empty content is rejected with INVALID_ARGUMENT
    Given the Chat service is running
    When I send a message with empty content
    Then the service returns status code INVALID_ARGUMENT
