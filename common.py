#!python

from __future__ import annotations
from typing import TYPE_CHECKING, Any

from datetime import datetime
from functools import cache

if TYPE_CHECKING:
    pass


@cache
def get_now() -> datetime:
    return datetime.now()


def get_datestr(dt: datetime) -> str:
    return dt.strftime("%d-%b-%Y")


Jobs = list[dict[str, Any]]
