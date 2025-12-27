from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class DspCoefficientsBlockData(Fmod5Sharp.ChunkData.IChunkData):
    def __init__(self, sampleMetadata: 'Fmod5Sharp.FmodTypes.FmodSampleMetadata') -> None: ...
    ChannelData: 'List[List[System.Int16]]' = ...
    def Read(self, reader: 'System.IO.BinaryReader', expectedSize: 'System.UInt32') -> None: ...

