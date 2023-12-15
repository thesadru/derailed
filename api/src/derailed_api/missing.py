from enum import Enum, auto
from typing import Literal, TypeVar

T = TypeVar("T")


class _Missing(Enum):
    MISSING = auto()

    def __bool__(self) -> Literal[False]:
        return False


MISSING: Literal[_Missing.MISSING] = _Missing.MISSING
Maybe = T | Literal[_Missing.MISSING]
