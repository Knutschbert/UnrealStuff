from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class ObjectHandle(System.MarshalByRefObject):
    def __init__(self, o: 'Any') -> None: ...
    def Unwrap(self) -> 'Any': ...

