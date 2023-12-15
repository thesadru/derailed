from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import any_pb2 as _any_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class Interchange(_message.Message):
    __slots__ = ["t", "id", "d"]
    T_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    t: str
    id: int
    d: str
    def __init__(
        self, t: _Optional[str] = ..., id: _Optional[int] = ..., d: _Optional[str] = ...
    ) -> None: ...

class BulkInterchange(_message.Message):
    __slots__ = ["t", "uids", "d"]
    T_FIELD_NUMBER: _ClassVar[int]
    UIDS_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    t: str
    uids: _containers.RepeatedScalarFieldContainer[int]
    d: _containers.RepeatedCompositeFieldContainer[Interchange]
    def __init__(
        self,
        t: _Optional[str] = ...,
        uids: _Optional[_Iterable[int]] = ...,
        d: _Optional[_Iterable[_Union[Interchange, _Mapping]]] = ...,
    ) -> None: ...

class GuildInfo(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GuildMetadata(_message.Message):
    __slots__ = ["available", "presences"]
    AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    PRESENCES_FIELD_NUMBER: _ClassVar[int]
    available: bool
    presences: int
    def __init__(
        self, available: bool = ..., presences: _Optional[int] = ...
    ) -> None: ...
