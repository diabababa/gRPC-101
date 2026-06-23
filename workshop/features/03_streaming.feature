Feature: Streaming Communication Patterns

  Scenario: Server streaming — retrieve chat history
    Given the Chat service is running
    And 3 messages were sent to room "streaming-history-01"
    When I request history for room "streaming-history-01" with limit 10
    Then I receive a stream of 3 messages

  Scenario: Server streaming respects the limit parameter
    Given the Chat service is running
    And 5 messages were sent to room "streaming-limit-01"
    When I request history for room "streaming-limit-01" with limit 2
    Then I receive a stream of 2 messages

  Scenario: Empty room returns no messages
    Given the Chat service is running
    When I request history for room "never-used-room" with limit 10
    Then I receive a stream of 0 messages

  Scenario: Client streaming — send bulk messages
    Given the Chat service is running
    When I stream 5 messages to room "streaming-bulk-01"
    Then the service reports 5 messages sent

  Scenario: Bidirectional streaming — Chat echoes each message back
    Given the Chat service is running
    When I send 3 messages through the bidirectional Chat stream to room "streaming-bidi-01"
    Then I receive 3 echoed messages back
