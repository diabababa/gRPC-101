Feature: Protocol Buffer Schema

  Scenario: Proto generates correct message types
    Given the proto schema is compiled
    When I inspect the generated module
    Then MessageRequest can be created with room_id, user, and content
    And MessageResponse has message_id, status, and timestamp fields
    And HistoryRequest has room_id and limit fields
    And Message has all five fields

  Scenario: ChatService stub has all four RPC methods
    Given the proto schema is compiled
    When I inspect the ChatServiceStub
    Then it has a "SendMessage" method
    And it has a "GetHistory" method
    And it has a "SendBulkMessages" method
    And it has a "Chat" method
