from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class EventNodesResolver:
    @staticmethod
    def ResolveAudioEvents(reader: 'CUE4Parse.UE4.FMod.FModReader') -> 'System.Collections.Generic.Dictionary[CUE4Parse.UE4.FMod.Objects.FModGuid, List[Fmod5Sharp.FmodTypes.FmodSample]]': ...
    @staticmethod
    def GetUnreferencedSamplesWithGuids(reader: 'CUE4Parse.UE4.FMod.FModReader', allResolved: 'System.Collections.Generic.HashSet[str]') -> 'System.Collections.Generic.Dictionary[CUE4Parse.UE4.FMod.Objects.FModGuid, Fmod5Sharp.FmodTypes.FmodSample]': ...
    @staticmethod
    def LogMissingSamples(reader: 'CUE4Parse.UE4.FMod.FModReader', resolvedEvents: 'System.Collections.Generic.Dictionary[CUE4Parse.UE4.FMod.Objects.FModGuid, List[Fmod5Sharp.FmodTypes.FmodSample]]') -> None: ...

