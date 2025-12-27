from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UNNEModelData(CUE4Parse.UE4.Assets.Exports.UObject, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...
    def Deserialize(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive', validPos: 'int') -> None: ...

class NNEModelDataVersion:
    GUID: 'CUE4Parse.UE4.Objects.Core.Misc.FGuid' = ...
    @staticmethod
    def Get(Ar: 'CUE4Parse.UE4.Readers.FArchive') -> 'CUE4Parse.UE4.Assets.Exports.NNE.NNEModelDataVersion.Type': ...

