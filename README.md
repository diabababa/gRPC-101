# Project Setup

## TODO: add QR code

clone repository: <strong>github.com/kamilkulig/grpc-101</strong>


```bash
# Clone & enter workshop
cd workshop

# run test-exercises
docker compose run --rm workshop poe test-solutions
docker compose run --rm workshop poe test-exercises

# Or create virtualenv and install deps and run
uv sync
source .venv/bin/activate
poe test-exercises
poe test-solutions
```


# gRPC for Beginners

https://github.com/KuligKamil/mongodb-project-workshop/

TODO: ADD QR CODE

Adam Gorgon - 

github: https://github.com/Ag0r9

linkedin: https://www.linkedin.com/in/adam-gorgon/

discord: gadamzaduzo

---

Kamil Kulig - Senior Backend Developer at cthings.co

github: https://github.com/KuligKamil

linkedin: https://www.linkedin.com/in/kamil-kulig-81488b89/

discord: kamilkulig

---


# What is gRPC (recursive acronym for gRPC Remote Procedure Calls)?

* High-performance alternative to REST APIs.

* **Remote Procedure Call** — call a function on another machine as if it were local.

  ```
  Client and Server have contract.

  Client                          Server
    |                               |
    |  sayHello("Alice")  ───────►  |
    |                               |  execute sayHello()
    |  ◄───────── "Hello, Alice!"   |
    |                               |
  ```

* By Google Open-sourced 2016, opence soruce [CNCF](https://en.wikipedia.org/wiki/Cloud_Native_Computing_Foundation)

* Supports multiple programming languages (C++, Java, Python, Go, C#, Ruby, Node.js, PHP, Dart, Kotlin, Rust, etc.)
  

---

# gRPC vs REST


| Aspect | REST API | gRPC |
|---------|------------|------|
| Protocol | HTTP/1.1 | HTTP/2 (Multiplexing *) |
| Format | JSON (text) | Binary format (Protobuf) |
| Performance | Good | Excellent (HTTP/2 + Protobuf) |
| Human readable | ✅  Yes | ❌ Binary |
| Streaming | Server-Sent Events (SSE), WebSocket, Long Polling | [Native] Server, Client, Bidirectional |
| Contract + Code gen | Optional | Protobuf |
| Browser support | ✅ Native | ❌ Needs grpc-web proxy |




*
Multiplexing means multiple streams — each carrying a request and response — can be sent simultaneously over a single connection, improving efficiency.
OR 
Multiplexing means that multiple independent streams — each representing a separate gRPC call — can be sent concurrently over a single TCP connection, with their frames interleaved, eliminating the need to open multiple connections and avoiding application-level head-of-line blocking present in HTTP/1.1.

# TODO: Locust show diffrence rest vs grpc  SHOW SOME NUMBER - COMPARISION


# When to Use gRPC


### ✅ Good fit

- Microservice-to-microservice communication.
- Real-time bidirectional streaming (chat, IoT, gaming).
- Polyglot environments (Python + Go + Java).
- High-throughput, low-latency APIs.
- Used by Google, Netflix, Square, Cisco, CockroachDB...

<!-- - Bandwidth-constrained clients — binary payloads use less data than JSON, matters on weak or metered connections (mobile data, IoT in the field, connected cars) -->


### ❌ Not the best fit

- Public APIs consumed by browsers directly.
- Simple CRUD with occasional calls.
- Teams unfamiliar with Protobuf.
- Debugging / human inspection of traffic.
- Simple scripts & one-off tools.
- Developer Experience is crucial.


Rule of thumb:
First REST API — better for external/public communication (partner APIs, browsers, simplicity). If you really need gRPC, then use it for internal communication (microservices, M2M, low latency);  gRPC between services, REST at the edge.

<!-- REST to styl architektoniczny (zbiór zasad), a nie konkretna technologia — nie da się go "użyć" wprost.
REST API to konkretna implementacja tego stylu (zwykle HTTP + JSON), czyli realny konkurent gRPC pod względem wydajności, formatu danych, itd. -->
<!-- Short rule of thumb: gRPC — great for internal communication (microservices, M2M, low latency); REST API — better for external/public communication (partner APIs, browsers, simplicity). -->


<!-- ### GRPC with Python  -->

<!-- To use it we need to install grpcio and grpcio-tools packages.  -->
<!-- https://github.com/vmagamedov/grpclib/issues/81#issuecomment-825697050
https://github.com/llucax/python-grpc-benchmark
This project is archived because grpclib's author said there are no plans for further development, so performance seems to be less important when choosing which library to use.
For async alternative is grpclib. But today we will not focus on it. We will use grpcio and grpcio-tools. -->



### Basics in gRPC 

Write a contract. Create .proto file use Protobuf.

Generate client and server stubs code with grpc_tools.protoc.

Implement server and call it from client.


LET'S CREATE SIMPLE PROJECT. Just watch, step by step I will explain what is going on. After DEMO you will do exercises.


# TODO: add screenshots from simple project.


<!--
10x / 3x — these are typical figures from Google's own benchmarks and community benchmarks
(e.g. github.com/thekvs/cpp-serializers). The actual gain depends on message structure:
flat, numeric-heavy messages compress more than deeply nested string-heavy ones.
Tell participants: "treat these as order-of-magnitude, benchmark your own workload."

Deadlines & cancellation:
- REST: if the client disconnects, the server keeps running (no built-in signal).
- gRPC: the client can attach a deadline (e.g. 500 ms). If the server hasn't finished
  by then, the call is cancelled on both sides automatically. context.is_active()
  returns False so you can stop early and free resources.
  This matters a lot for streaming — you don't leak open streams when clients drop.
-->


---

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

# Project Setup

## TODO: add QR code

clone repository: <strong>github.com/kamilkulig/grpc-101</strong>


```bash
# Clone & enter workshop
cd workshop

# run test-exercises
docker compose run --rm workshop poe test-solutions
docker compose run --rm workshop poe test-exercises

# Or create virtualenv and install deps and run
uv sync
source .venv/bin/activate
poe test-exercises
poe test-solutions
```


# unary


# server_streaming


# client_streaming


# bidirectional_streaming


# error_handling_and_status_codes


# cancellation_and_deadlines


# production


# summary


# go_deepER
Adam

# resources


# Q&A
