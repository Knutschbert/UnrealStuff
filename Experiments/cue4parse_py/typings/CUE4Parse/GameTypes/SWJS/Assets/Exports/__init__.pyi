from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class URsColorGradeTexture(CUE4Parse.UE4.Assets.Exports.Texture.UTexture2D, CUE4Parse.UE4.Assets.Exports.IPropertyHolder, CUE4Parse.UE4.Assets.Exports.Component.IAssetUserData):
    def __init__(self) -> None: ...

class URsWorldMapStaticMeshComponent(CUE4Parse.UE4.Assets.Exports.Component.StaticMesh.UStaticMeshComponent, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class URsWorldMapInstancedStaticMeshComponent(CUE4Parse.UE4.Assets.Exports.Component.StaticMesh.UInstancedStaticMeshComponent, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

