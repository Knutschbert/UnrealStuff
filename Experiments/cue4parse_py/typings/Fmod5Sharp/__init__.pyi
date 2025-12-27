from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FsbLoader:
    @staticmethod
    def TryLoadFsbFromByteArray(bankBytes: 'List[int]') -> Tuple['bool', 'Fmod5Sharp.FmodTypes.FmodSoundBank']: ...
    @staticmethod
    def LoadFsbFromByteArray(bankBytes: 'List[int]') -> 'Fmod5Sharp.FmodTypes.FmodSoundBank': ...

from . import Util as Util
from . import FmodTypes as FmodTypes
from . import CodecRebuilders as CodecRebuilders
from . import ChunkData as ChunkData
