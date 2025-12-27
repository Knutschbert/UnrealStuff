from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class IUStruct:
    pass

from . import Wwise as Wwise
from . import Writers as Writers
from . import VirtualFileSystem as VirtualFileSystem
from . import VirtualFileCache as VirtualFileCache
from . import Versions as Versions
from . import Shaders as Shaders
from . import Readers as Readers
from . import Plugins as Plugins
from . import Oodle as Oodle
from . import Objects as Objects
from . import Localization as Localization
from . import Kismet as Kismet
from . import IO as IO
from . import FMod as FMod
from . import Exceptions as Exceptions
from . import CriWare as CriWare
from . import BinaryConfig as BinaryConfig
from . import AssetRegistry as AssetRegistry
from . import Assets as Assets
from . import Pak as Pak
