from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class InvalidAesKeyException(CUE4Parse.UE4.Exceptions.ParserException, System.Runtime.Serialization.ISerializable):
    @overload
    def __init__(self, message: 'str', innerException: 'System.Exception') -> None: ...
    @overload
    def __init__(self, reader: 'CUE4Parse.UE4.Readers.FArchive', message: 'str', innerException: 'System.Exception') -> None: ...

class ParserException(System.Exception, System.Runtime.Serialization.ISerializable):
    @overload
    def __init__(self, message: 'str', innerException: 'System.Exception') -> None: ...
    @overload
    def __init__(self, reader: 'CUE4Parse.UE4.Readers.FArchive', message: 'str', innerException: 'System.Exception') -> None: ...

class UnknownCompressionMethodException(CUE4Parse.UE4.Exceptions.ParserException, System.Runtime.Serialization.ISerializable):
    @overload
    def __init__(self, message: 'str', innerException: 'System.Exception') -> None: ...
    @overload
    def __init__(self, reader: 'CUE4Parse.UE4.Readers.FArchive', message: 'str', innerException: 'System.Exception') -> None: ...

