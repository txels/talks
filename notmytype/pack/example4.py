from typing import Callable, Sized

ProcessCallback = Callable[[Sized, int], bool]


def process_item(item: str, callback: ProcessCallback) -> None:
    callback(item, 3)


def suitable_callback(name: Sized, expected_len: int) -> bool:
    return len(name) == expected_len


def unsuitable_callback(name: str) -> int:
    return len(name)


process_item("potato", suitable_callback)
process_item("potato", unsuitable_callback)
