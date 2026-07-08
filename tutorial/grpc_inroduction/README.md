# What is gRPC - Google Remote Procedure Call ?

* High-performance alternative to REST APIs.

<!-- TOOD maybe remove it -->
<!-- * For M2M communication. but not only. -->

* Google **Remote Procedure Call** — call a function on another machine as if it were local.

  ```
  Client and Server have contract.

  Client                          Server
    |                               |
    |  sayHello("Alice")  ───────►  |
    |                               |  execute sayHello()
    |  ◄───────── "Hello, Alice!"   |
    |                               |
  ```

* Open-sourced 2016, opence soruce [CNCF](https://en.wikipedia.org/wiki/Cloud_Native_Computing_Foundation)


# gRPC vs REST


| Aspect | REST API | gRPC |
|---------|------------|------|
| Protocol | HTTP/1.1 | HTTP/2 (Multiplexing) |
| Format | JSON (text) | Binary format (Protobuf) |
| Performance | Good | Excellent (HTTP/2 + Protobuf) |
| Human readable | ✅  Yes | ❌ Binary |
| Streaming | Server-Sent Events (SSE), WebSocket, Long Polling | [Native] Server, Client, Bidirectional |
| Contract + Code gen | Optional | Protobuf |
| Browser support | ✅ Native | ❌ Needs grpc-web proxy |

TOOD: SHOW SOME NUMBER - COMPARISION


# When to Use gRPC


### ✅ Good fit

- Microservice-to-microservice communication.
- Real-time bidirectional streaming (chat, IoT, gaming).
- Polyglot environments (Python + Go + Java).
- High-throughput, low-latency APIs.
<!-- - Bandwidth-constrained clients — binary payloads use less data than JSON, matters on weak or metered connections (mobile data, IoT in the field, connected cars) -->


### ❌ Not the best fit

- Public APIs consumed by browsers directly.
- Simple CRUD with occasional calls.
- Teams unfamiliar with Protobuf.
- Debugging / human inspection of traffic.
- Simple scripts & one-off tools.
- Developer Experience is crucial.



Rule of thumb: gRPC between services, REST at the edge
Short rule of thumb: gRPC — great for internal communication (microservices, M2M, low latency); REST API — better for external/public communication (partner APIs, browsers, simplicity).


<!-- REST to styl architektoniczny (zbiór zasad), a nie konkretna technologia — nie da się go "użyć" wprost.
REST API to konkretna implementacja tego stylu (zwykle HTTP + JSON), czyli realny konkurent gRPC pod względem wydajności, formatu danych, itd. -->
<!-- Short rule of thumb: gRPC — great for internal communication (microservices, M2M, low latency); REST API — better for external/public communication (partner APIs, browsers, simplicity). -->


<!-- Multiplexing is sending multiple independent data streams over a single network connection simultaneously, instead of opening a separate connection for each request. -->

### Basics in gRPC 

Write a contract. Create .proto file use Protobuf.

Generate client and server stubs code with grpc_tools.protoc.

Implement server and call it from client.


LET'S CREATE SIMPLE PROJECT.


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