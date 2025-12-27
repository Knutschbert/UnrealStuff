from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FmodAudioTypeExtensions:
    @staticmethod
    def IsSupported(this: 'Fmod5Sharp.FmodTypes.FmodAudioType') -> 'bool': ...
    @staticmethod
    def FileExtension(this: 'Fmod5Sharp.FmodTypes.FmodAudioType') -> 'str': ...

