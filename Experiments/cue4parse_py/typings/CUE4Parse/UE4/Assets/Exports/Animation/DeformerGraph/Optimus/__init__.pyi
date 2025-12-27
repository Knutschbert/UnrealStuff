from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class UOptimusComputeGraph(CUE4Parse.UE4.Assets.Exports.ComputerFramework.UComputeGraph, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UOptimusNode_ComputeKernelFunctionGeneratorClass(CUE4Parse.UE4.Objects.UObject.UClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UOptimusNode_ConstantValueGeneratorClass(CUE4Parse.UE4.Objects.UObject.UClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

class UOptimusValueContainerGeneratorClass(CUE4Parse.UE4.Objects.UObject.UClass, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...

