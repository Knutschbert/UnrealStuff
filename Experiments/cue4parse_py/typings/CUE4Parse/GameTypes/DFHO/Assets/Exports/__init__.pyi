from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UVirtualMaterialInstanceConstant(CUE4Parse.UE4.Assets.Exports.Material.UMaterialInstanceConstant, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UStaticLabelMesh(CUE4Parse.UE4.Assets.Exports.StaticMesh.UStaticMesh, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class USMBlueprintGeneratedClass(CUE4Parse.UE4.Objects.Engine.UBlueprintGeneratedClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class USMNodeBlueprintGeneratedClass(CUE4Parse.UE4.Objects.Engine.UBlueprintGeneratedClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

