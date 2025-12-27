from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UInstancedCoverageMeshComponent(CUE4Parse.UE4.Assets.Exports.Component.StaticMesh.UStaticMeshComponent, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...
    def GetStaticMesh(self) -> 'CUE4Parse.UE4.Objects.UObject.FPackageIndex': ...

