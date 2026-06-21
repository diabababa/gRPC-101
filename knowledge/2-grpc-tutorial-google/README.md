TODO: add it to the list 



https://docs.python.org/3/library/ensurepip.html


ensurepip is a module in Python that provides support for bootstrapping the pip installer into an existing Python installation. It allows you to install pip and its dependencies without needing to download and run the get-pip.py script separately.

TODO: add it to the tutorial
not forgot about `uv self update` 

source .venv/bin/activate


TODO: Question what ot use to open .proto files? in vs code
deprecated: https://marketplace.visualstudio.com/items?itemName=zxh404.vscode-proto3
https://marketplace.visualstudio.com/items?itemName=BruceWu.proto-navigation

https://marketplace.visualstudio.com/items?itemName=bufbuild.vscode-buf&ssr=false#overview

`curl -sL https://github.com/grpc-ecosystem/grpc-codelabs/archive/refs/heads/v1.tar.gz \
  | tar xvz --strip-components=4 \
  grpc-codelabs-1/codelabs/grpc-python-streaming/start_here`


Use the following command to generate the Python boilerplate code:


python -m grpc_tools.protoc --proto_path=./protos  \
 --python_out=. --pyi_out=. --grpc_python_out=. \
 ./protos/route_guide.proto
This will generate the following files for the interfaces we defined in route_guide.proto:

route_guide_pb2.py contains the code that dynamically creates classes generated from the message definitions.
route_guide_pb2.pyi is a "stub file" or "type hint file" generated from the message definitions. It only contains the signatures with no implementation. Stub files can be used by IDEs to provide better autocompletion and error detection.
route_guide_pb2_grpc.py is generated from the service definitions and contains gRPC-specific classes and functions.

Observation: 
The code generation process is deterministic - when you re-run the protoc command with the same .proto files, it will always generate identical output, which ensures consistency across your development team and in CI/CD pipelines.

