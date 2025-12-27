from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UVectorField(CUE4Parse.UE4.Assets.Exports.UObject, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UVectorFieldStatic(CUE4Parse.UE4.Objects.Engine.VectorField.UVectorField, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...
    SourceData: 'CUE4Parse.UE4.Assets.Objects.FByteBulkData' = ...
    def Deserialize(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive', validPos: 'int') -> None: ...

