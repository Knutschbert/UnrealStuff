from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class ULevelSequence(CUE4Parse.UE4.Assets.Exports.MovieScene.UMovieSceneSequence, CUE4Parse.UE4.Assets.Exports.IPropertyHolder):
    def __init__(self) -> None: ...
    MovieScene: 'CUE4Parse.UE4.Objects.UObject.FPackageIndex' = ...
    def Deserialize(self, Ar: 'CUE4Parse.UE4.Assets.Readers.FAssetArchive', validPos: 'int') -> None: ...

