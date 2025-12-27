from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UCustomBendClass(CUE4Parse.UE4.Assets.Exports.UObject, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...
    def Deserialize(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive', validPos: 'int') -> None: ...

class UBendBlockingVolumeCollectionComponent(CUE4Parse.GameTypes.DaysGone.Assets.Exports.UCustomBendClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UBendDecalCollectionComponent(CUE4Parse.GameTypes.DaysGone.Assets.Exports.UCustomBendClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UBendNavLinkCollectionComponent(CUE4Parse.GameTypes.DaysGone.Assets.Exports.UCustomBendClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UBendStaticMeshCollectionComponent(CUE4Parse.GameTypes.DaysGone.Assets.Exports.UCustomBendClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

