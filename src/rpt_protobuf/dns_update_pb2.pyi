import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from rpt_protobuf import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class dns_update(_message.Message):
    __slots__ = ("timestamp", "node")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    node: _node_pb2.node
    def __init__(self, timestamp: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., node: _Optional[_Union[_node_pb2.node, _Mapping]] = ...) -> None: ...
