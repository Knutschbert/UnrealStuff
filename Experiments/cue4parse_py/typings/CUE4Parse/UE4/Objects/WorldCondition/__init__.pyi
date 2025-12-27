from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FWorldConditionCustomVersion:
    GUID: 'CUE4Parse.UE4.Objects.Core.Misc.FGuid' = ...
    @staticmethod
    def Get(Ar: 'CUE4Parse.UE4.Readers.FArchive') -> 'CUE4Parse.UE4.Objects.WorldCondition.FWorldConditionCustomVersion.Type': ...

class FWorldConditionQueryDefinition(CUE4Parse.UE4.IUStruct):
    def __init__(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive') -> None: ...
    StaticStruct: 'CUE4Parse.UE4.Assets.Objects.FStructFallback' = ...
    SharedDefinition: 'CUE4Parse.UE4.Assets.Objects.FStructFallback' = ...

