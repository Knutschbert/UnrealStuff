from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class SOD2Properties:
    @staticmethod
    def GetMapPropertyTypes(name: 'str') -> 'System.ValueTuple[str, str]': ...

from . import Objects as Objects
