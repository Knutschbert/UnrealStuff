from __future__ import annotations
from typing import Any, List, Dict, Optional, overload, TypeVar, Generic, Tuple
import enum, System, CUE4Parse
T = TypeVar('T')
class Lazy(Generic[T]): value: T
Nullable = Optional

class FrozenDictionary:
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[System.Collections.Generic.KeyValuePair[TKey, TValue]]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TValue]': ...
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[TSource]', keySelector: 'System.Func[TSource, TKey]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TSource]': ...
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[TSource]', keySelector: 'System.Func[TSource, TKey]', elementSelector: 'System.Func[TSource, TElement]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TElement]': ...

class FrozenSet:
    @staticmethod
    @overload
    def Create(source: 'System.ReadOnlySpan[T]') -> 'FrozenSet[T]': ...
    @staticmethod
    @overload
    def Create(equalityComparer: 'System.Collections.Generic.IEqualityComparer[T]', source: 'System.ReadOnlySpan[T]') -> 'FrozenSet[T]': ...
    @staticmethod
    def ToFrozenSet(source: 'List[T]', comparer: 'System.Collections.Generic.IEqualityComparer[T]') -> 'FrozenSet[T]': ...

class FrozenDictionary:
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[System.Collections.Generic.KeyValuePair[TKey, TValue]]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TValue]': ...
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[TSource]', keySelector: 'System.Func[TSource, TKey]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TSource]': ...
    @staticmethod
    @overload
    def ToFrozenDictionary(source: 'List[TSource]', keySelector: 'System.Func[TSource, TKey]', elementSelector: 'System.Func[TSource, TElement]', comparer: 'System.Collections.Generic.IEqualityComparer[TKey]') -> 'FrozenDictionary[TKey, TElement]': ...

class FrozenSet:
    @staticmethod
    @overload
    def Create(source: 'System.ReadOnlySpan[T]') -> 'FrozenSet[T]': ...
    @staticmethod
    @overload
    def Create(equalityComparer: 'System.Collections.Generic.IEqualityComparer[T]', source: 'System.ReadOnlySpan[T]') -> 'FrozenSet[T]': ...
    @staticmethod
    def ToFrozenSet(source: 'List[T]', comparer: 'System.Collections.Generic.IEqualityComparer[T]') -> 'FrozenSet[T]': ...

