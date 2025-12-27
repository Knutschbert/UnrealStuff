from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class Console:
    @staticmethod
    @overload
    def WriteLine(s: 'str') -> None: ...
    @staticmethod
    @overload
    def WriteLine() -> None: ...
    @staticmethod
    def Write(s: 'str') -> None: ...

from . import Win32 as Win32
from . import Runtime as Runtime
from . import NativeCrypto as NativeCrypto
from . import Cryptography as Cryptography
