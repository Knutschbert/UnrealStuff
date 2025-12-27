from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class RennsportAes:
    @staticmethod
    @overload
    def RennsportDecrypt(bytes: 'List[int]', beginOffset: 'int', count: 'int', isIndex: 'bool', reader: 'CUE4Parse.UE4.VirtualFileSystem.IAesVfsReader') -> 'List[int]': ...
    @staticmethod
    @overload
    def RennsportDecrypt(bytes: 'List[int]', beginOffset: 'int', count: 'int', isIndex: 'bool', reader: 'CUE4Parse.UE4.VirtualFileSystem.IAesVfsReader', directoryIndex: 'bool') -> 'List[int]': ...

