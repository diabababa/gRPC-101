Feature: Service Performance Under Load

  Scenario: Service handles 50 concurrent SendMessage requests
    Given the Chat service is running
    When I send 50 messages concurrently with 10 worker threads to room "perf-concurrent"
    Then all requests succeed
    And the average response time is under 500ms

  Scenario: Service maintains stability under sequential load
    Given the Chat service is running
    When I send 30 messages sequentially to room "perf-sequential"
    Then all requests succeed
