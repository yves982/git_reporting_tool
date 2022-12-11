# -*- coding: utf-8 -*-
from typing import List, Callable, TypeVar

T = TypeVar("T")


def assert_collection_equivalent(actual: List[T], expected: List[T], item_name: str,
                                 item_comparer: Callable[[T, T], int]):
    actual_len = len(actual)
    expected_len = len(expected)
    assert actual_len == expected_len, f"collections length were different! found {actual_len}," \
                                       f" expected {expected_len} ({item_name})"
    for index, item in enumerate(actual):
        assert item_comparer(item, expected[index]) == 0
