from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class PMAAes:
    def __init__(self) -> None: ...
    @staticmethod
    def PMADecrypt(bytes: 'List[int]', beginOffset: 'int', count: 'int', isIndex: 'bool', reader: 'CUE4Parse.UE4.VirtualFileSystem.IAesVfsReader') -> 'List[int]': ...

