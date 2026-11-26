from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class node(_message.Message):
    __slots__ = ("id", "ipaddress", "port", "ttl", "server")
    ID_FIELD_NUMBER: _ClassVar[int]
    IPADDRESS_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    TTL_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    id: int
    ipaddress: str
    port: int
    ttl: int
    server: str
    def __init__(self, id: _Optional[int] = ..., ipaddress: _Optional[str] = ..., port: _Optional[int] = ..., ttl: _Optional[int] = ..., server: _Optional[str] = ...) -> None: ...
