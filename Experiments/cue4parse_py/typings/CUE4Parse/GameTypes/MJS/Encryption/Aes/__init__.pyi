from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class MonsterJamShowdownAes:
    @staticmethod
    def MonsterJamShowdownDecrypt(bytes: 'List[int]', beginOffset: 'int', count: 'int', isIndex: 'bool', reader: 'CUE4Parse.UE4.VirtualFileSystem.IAesVfsReader') -> 'List[int]': ...

class MotoGP25Aes:
    @staticmethod
    def MotoGP25Decrypt(bytes: 'List[int]', beginOffset: 'int', count: 'int', isIndex: 'bool', reader: 'CUE4Parse.UE4.VirtualFileSystem.IAesVfsReader') -> 'List[int]': ...

