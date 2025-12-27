from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FNavAgentSelector(System.ValueType, CUE4Parse.UE4.IUStruct):
    PackedBits: 'System.UInt32' = ...

