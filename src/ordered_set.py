# type: ignore
from dataclasses import dataclass, field
from itertools import islice
from typing import Dict, Iterable, Iterator, List, MutableSet, TypeVar

T = TypeVar("T")


@dataclass(order=True)
class OrderedSet(MutableSet[T]):
    data: Iterable[T]
    _data: Dict[T, None] = field(repr=False, init=False)

    #  Mypy doesn't like getters and setters
    @property  # type: ignore
    def data(self) -> List[T]:
        return list(self._data)

    @data.setter
    def data(self, d: Iterable[T]):
        self._data = dict.fromkeys(d)

    def add(self, x: T) -> None:
        self._data[x] = None

    def discard(self, x: T) -> None:
        self._data.pop(x, None)

    def __getitem__(self, index: int) -> T:
        try:
            return next(islice(self._data, index, index + 1))
        except StopIteration:
            raise IndexError(f"index {index} out of range")

    def __contains__(self, x: object) -> bool:
        return self._data.__contains__(x)

    def __len__(self) -> int:
        return self._data.__len__()

    def __iter__(self) -> Iterator[T]:
        return self._data.__iter__()
