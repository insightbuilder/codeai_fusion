#!/bin/bash

# Generate gRPC Python files
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. store.proto

echo "gRPC Python files generated successfully!"
