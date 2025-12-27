from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

from . import NonGeneric as NonGeneric
from . import Specialized as Specialized
from . import Immutable as Immutable
