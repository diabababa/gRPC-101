# Exercise 4: Testing — pytest + Gherkin (20 min)

## Goal

Two tasks in one:

**Part A** — Write classic **pytest** tests in `test_starter.py`  
**Part B** — Write **Gherkin scenarios** in `chat_starter.feature`

Both test the same service — compare how the two styles feel.

## What is Gherkin?

Gherkin is the language of BDD (Behaviour-Driven Development). Scenarios are written in:

```gherkin
Scenario: <what you're testing>
  Given <initial context>
  When  <action>
  Then  <expected outcome>
  And   <more outcomes>
```

The key idea: scenarios are readable by non-developers and serve as living documentation.

## Your task

Open `chat_starter.feature` and fill in the `TODO` scenarios.

### Available steps you can use

```gherkin
# Setup
Given the Chat service is running

# Send a single message
When I send a message to room "my-room" as user "alice" with content "Hello!"
When I send a message with empty content

# Assertions for SendMessage
Then I receive a response with a non-empty message_id
Then the response status is "ok"
Then the response has a positive timestamp
Then the service returns status code INVALID_ARGUMENT

# History (server streaming)
Given 3 messages were sent to room "my-room"
When I request history for room "my-room" with limit 10
Then I receive a stream of 3 messages

# Bulk send (client streaming)
When I stream 5 messages to room "my-room"
Then the service reports 5 messages sent

# Bidirectional
When I send 3 messages through the bidirectional Chat stream to room "my-room"
Then I receive 3 echoed messages back
```

## Run

```bash
# Part A — your pytest tests
pytest exercises/04_gherkin/test_starter.py -v

# Part B — your Gherkin scenarios (loaded by poe test-exercises)
pytest tests/step_defs/test_04_gherkin.py -v

# Both at once
poe test-exercises
```

## Solution

`solutions/04_gherkin/chat.feature`
