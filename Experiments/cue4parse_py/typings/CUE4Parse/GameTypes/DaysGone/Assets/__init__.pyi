from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class DaysGoneProperties:
    @staticmethod
    def GetMapPropertyTypes(name: 'str') -> 'System.ValueTuple[str, str]': ...
    @staticmethod
    def GetArrayStructType(name: 'str', elementSize: 'int') -> 'CUE4Parse.UE4.Assets.Objects.FPropertyTagData': ...

from . import Exports as Exports
