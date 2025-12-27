from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FCore1047ReleaseFlag(System.ValueType, CUE4Parse.UE4.IUStruct):
    def __init__(self, Ar: 'CUE4Parse.UE4.Readers.FArchive') -> None: ...
    Release: 'CUE4Parse.UE4.Objects.UObject.FName' = ...

