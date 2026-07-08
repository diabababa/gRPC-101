# Protocol Buffers — The Language of gRPC

**Protobuf** is a language-neutral schema language and binary serialization format.


```proto

syntax = "proto3";

package shop;

import "google/protobuf/timestamp.proto";

message Order {
  string order_id = 1;
  repeated Item items = 2;
  map<string, string> metadata = 3;   // e.g., "coupon" -> "SUMMER10"

  google.protobuf.Timestamp created_at = 4;

  Status status = 5;

  // oneof = "pay card, or BLIK, never both at once"
  oneof payment_method {
    CardPayment card = 6;
    BlikPayment blik = 7;
  }

  reserved 8, 9;          //  reserved field numbers
  reserved "legacy_note"; // reserved field names 
  // reserved fields are for backward compatibility, to avoid reusing field numbers or names that were used in previous versions of the schema


  message Item {
    string product_id = 1;
    int32 quantity = 2;
    double unit_price = 3;
  }

  enum Status {
    UNKNOWN = 0;
    PENDING = 1;
    PAID = 2;
    SHIPPED = 3;
    CANCELLED = 4;
  }
}

message CardPayment {
  string last4 = 1;
}

message BlikPayment {
  string code = 1;
}

service OrderService {
  // response - request (unary)
  rpc PlaceOrder (Order) returns (OrderConfirmation);

  // server streaming – tracking order status in real-time
  rpc TrackOrder (OrderId) returns (stream OrderStatusUpdate);
}

message OrderId {
  string order_id = 1;
}

message OrderConfirmation {
  string order_id = 1;
  bool accepted = 2;
}

message OrderStatusUpdate {
  Order.Status status = 1;
  google.protobuf.Timestamp updated_at = 2;
}

```


<!-- 
- Field numbers (1, 2, 3…) identify fields in binary — **never change them**
- Types: `string`, `int32`, `int64`, `bool`, `float`, `double`, `bytes`
- Collections: `repeated string tags = 4;`. Without `repeated`, a variable can have only one value
- Optional fields (proto3): all fields are optional by default 
-->
  

---