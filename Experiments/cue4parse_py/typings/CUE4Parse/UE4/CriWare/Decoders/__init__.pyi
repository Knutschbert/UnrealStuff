from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class CriwareDecryptionException(System.Exception, System.Runtime.Serialization.ISerializable):
    @overload
    def __init__(self, message: 'str') -> None: ...
    @overload
    def __init__(self, message: 'str', inner: 'System.Exception') -> None: ...

class CriCipherUtil:
    @staticmethod
    def EmbedSubKey(stream: 'System.IO.Stream', subKey: 'System.UInt16') -> 'List[int]': ...
    @staticmethod
    def ExtractSubKey(data: 'List[int]') -> 'System.ValueTuple[System.UInt16, List[int]]': ...

from . import HCA as HCA
from . import ADX as ADX
