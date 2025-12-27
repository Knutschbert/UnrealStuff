from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FmodGcadPcmRebuilder:
    @staticmethod
    def Rebuild(sample: 'Fmod5Sharp.FmodTypes.FmodSample') -> 'List[int]': ...

class FmodImaAdPcmRebuilder:
    SamplesPerFramePerChannel: 'int' = ...
    @staticmethod
    def Rebuild(sample: 'Fmod5Sharp.FmodTypes.FmodSample') -> 'List[int]': ...

class FmodPcmRebuilder:
    @staticmethod
    def Rebuild(sample: 'Fmod5Sharp.FmodTypes.FmodSample', type: 'Fmod5Sharp.FmodTypes.FmodAudioType') -> 'List[int]': ...

class FmodVorbisRebuilder:
    @staticmethod
    def RebuildOggFile(sample: 'Fmod5Sharp.FmodTypes.FmodSample') -> 'List[int]': ...

