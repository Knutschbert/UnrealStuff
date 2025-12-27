from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class ObjectiveCMarshal:
    @staticmethod
    def Initialize(beginEndCallback: '', isReferencedCallback: '', trackedObjectEnteredFinalization: '', unhandledExceptionPropagationHandler: 'System.Runtime.InteropServices.ObjectiveC.ObjectiveCMarshal.UnhandledExceptionPropagationHandler') -> None: ...
    @staticmethod
    def CreateReferenceTrackingHandle(obj: 'Any') -> Tuple['System.Runtime.InteropServices.GCHandle', 'System.Span_1[[System.IntPtr, System.Private.CoreLib, Version=9.0.0.0, Culture=neutral, PublicKeyToken=7cec85d7bea7798e]]']: ...
    @staticmethod
    def SetMessageSendCallback(msgSendFunction: 'System.Runtime.InteropServices.ObjectiveC.ObjectiveCMarshal.MessageSendFunction', func: 'System.IntPtr') -> None: ...
    @staticmethod
    def SetMessageSendPendingException(exception: 'System.Exception') -> None: ...

class ObjectiveCTrackedTypeAttribute(System.Attribute):
    def __init__(self) -> None: ...

