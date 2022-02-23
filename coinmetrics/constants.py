from enum import Enum


class PagingFrom(Enum):
    START = "start"
    END = "end"


class Backfill(Enum):
    LATEST = "latest"
    NONE = "none"
