from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FTslSomeSKStruct(CUE4Parse.UE4.IUStruct):
    def __init__(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive') -> None: ...
    SomeBoneStructs: 'List[List[System.Collections.Generic.Dictionary[CUE4Parse.GameTypes.PUBG.Assets.Objects.FTslSomeBoneStruct, CUE4Parse.GameTypes.PUBG.Assets.Objects.FTslSomeBoneStruct]]]' = ...

class FTslSomeBoneStruct(System.ValueType):
    Type: 'int' = ...
    Bone: 'int' = ...

