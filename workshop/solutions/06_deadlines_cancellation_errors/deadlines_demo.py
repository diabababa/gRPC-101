"""Solution — Exercise 6: deadlines, cancellation, and error handling.

Run your solution server first:
    poe server-solutions
"""

import grpc

from solutions.generated import chat_pb2, chat_pb2_grpc

SOLUTION_SERVER = "localhost:50051"
UNREACHABLE_SERVER = "localhost:50099"


def _format_rpc_error(error: grpc.RpcError) -> str:
    return f"code={error.code().name} details={error.details()}"


def demo_deadline_exceeded() -> grpc.StatusCode:
    print("\n[Deadline]")
    with grpc.insecure_channel(UNREACHABLE_SERVER) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        try:
            stub.SendMessage(
                chat_pb2.MessageRequest(
                    room_id="deadline-room",
                    user="alice",
                    content="This will hit deadline",
                ),
                timeout=0.2,
                wait_for_ready=True,
            )
            print("unexpected success")
            return grpc.StatusCode.OK
        except grpc.RpcError as error:
            print(_format_rpc_error(error))
            return error.code()


def demo_client_cancellation() -> bool:
    print("\n[Cancel]")
    with grpc.insecure_channel(UNREACHABLE_SERVER) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        future = stub.SendMessage.future(
            chat_pb2.MessageRequest(
                room_id="cancel-room",
                user="alice",
                content="cancel me",
            ),
            timeout=10,
            wait_for_ready=True,
        )
        cancelled = future.cancel()
        print(f"cancelled={cancelled}")
        return cancelled


def demo_invalid_argument() -> grpc.StatusCode:
    print("\n[Error]")
    with grpc.insecure_channel(SOLUTION_SERVER) as channel:
        stub = chat_pb2_grpc.ChatServiceStub(channel)
        try:
            stub.SendMessage(
                chat_pb2.MessageRequest(
                    room_id="general",
                    user="alice",
                    content="",
                )
            )
            print("unexpected success")
            return grpc.StatusCode.OK
        except grpc.RpcError as error:
            print(_format_rpc_error(error))
            return error.code()


def main() -> None:
    demo_deadline_exceeded()
    demo_client_cancellation()
    demo_invalid_argument()


if __name__ == "__main__":
    main()
