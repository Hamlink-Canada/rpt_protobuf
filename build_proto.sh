#!/bin/sh

# protoc --python_out output protobuf/dns.proto

protoc \
    -I./protos \
    --python_out=protobuf/ \
    --grpc_python_out=protobuf/ \
    --plugin=protoc-gen-grpc_python=$(which grpc_python_plugin) \
    ./protos/*.proto
