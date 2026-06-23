Feature: Chat Service — Gherkin Practice
# ============================================================
# Exercise 4: Fill in the TODO scenarios below.
#
# Step definitions are already implemented — you only write Gherkin.
# Run:  poe test-exercises
# ============================================================

  # This scenario is done for you as an example:
  Scenario: Send a message successfully
    Given the Chat service is running
    When I send a message to room "gherkin-demo" as user "workshop" with content "Hello Gherkin!"
    Then I receive a response with a non-empty message_id
    And the response status is "ok"

  # TODO: Write a scenario that tests sending a message with empty content.
  # Expected: the service should reject it with INVALID_ARGUMENT.

  # TODO: Write a scenario for GetHistory (server streaming).
  # Hint: first seed some messages with "Given N messages were sent to room ...",
  #       then request history and assert you get the right number back.

  # TODO (Bonus): Write a scenario for sending bulk messages (client streaming).
  # Hint: use "When I stream N messages to room ..." and
  #       "Then the service reports N messages sent".
