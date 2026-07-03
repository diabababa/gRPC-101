import os
import shutil

order = (
    "introduction",
    "why_mongodb",
    "python_mongodb_tools",
    "project_setup",
    "mongodb_atlas",
    "documents_database",
    "connection_to_db",
    "data_structure",
    "data_generators",
    "simple_queries_atlas",
    "crud_queries",
    "tests",
    "resources",
)
order = (
    "workshop_instructor_introduction",
    "grpc_inroduction",
    # "what_is_RPC",
    # "what_is_gRPC", gRPC is designed to support high-performance open-source RPCs in many languages.
    # "why_not_X", REST VS gRPC
    # "gRPC_service&4patterns",
    # "why_gRPC",
    # "locust_and_results_compering_to_different_tech",
    # "tools for gRPC",
    "project_setup",
    # "what_project_are_we_building", !!!
    "protobuf",  # Protocol Buffers
    "create_proto_messages",
    "create_service_stubs",
    # diff service vs server
    "unary",
    "server_streaming",
    "client_streaming",
    "bidirectional_streaming",
    # "create_service",
    # # "create_service_stub",
    # # "implement_service_stub",
    # "create_client",
    # # "how_to_implement_4_patterns_to_clientexercise5_implement_4_patterns_to_client",
    "error_handling&status_codes",
    "cancellation&deadlines",
    # TODO: add more: next guides https://grpc.io/docs/guides/
    "production",
    # "metadata&interceptors",
    # Authentication
    # Graceful Shutdown
    # Health Checking
    # Reflaction
    # Monitoring
    "summary",
    "go deepER",
    "resources",
    "Q&A",
)


project_directory = os.getcwd()
new_line = "\n"
if os.path.exists(f"{project_directory}/README.md"):
    os.remove(f"{project_directory}/README.md")
for index, tutorial_chapter in enumerate(order):
    temp_text = ""
    with open(
        os.path.join(f"{project_directory}/tutorial/{tutorial_chapter}", "README.md")
    ) as f:
        temp_text = f.read()

    # check = re.search(r"\`\`\`python(.*?)\`", temp_text)
    # if check:
    #     print(check.group(0))
    # print(check)
    # print(type(check))
    with open(f"{project_directory}/README.md", "a") as f:
        f.write(f"{new_line * 2 if index > 0 else ''}{temp_text}")


project_directory = os.getcwd()
for root, _, files in os.walk(f"{project_directory}/assets"):
    for file in files:
        os.remove(os.path.join(root, file))
for root, _, f in os.walk(f"{project_directory}/tutorial"):
    for file in f:
        # print(root, _, f, file)
        directory = root.split("/")[-1]
        if directory == "assets":
            shutil.copyfile(
                os.path.join(root, file),
                os.path.join(f"{project_directory}/assets/{file}"),
            )
