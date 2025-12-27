from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FStateTreeInstanceData(CUE4Parse.UE4.IUStruct):
    def __init__(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive') -> None: ...
    Data: 'CUE4Parse.UE4.Assets.Objects.FStructFallback' = ...

