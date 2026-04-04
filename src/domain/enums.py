from enum import Enum


class StockState(Enum):
    """Normalized stock states for products."""

    UNKNOWN = "UNKNOWN"
    UNAVAILABLE = "UNAVAILABLE"
    COMING_SOON = "COMING_SOON"
    NOTIFY_ME = "NOTIFY_ME"
    LOW_STOCK = "LOW_STOCK"
    IN_STOCK = "IN_STOCK"
    FETCH_FAILED = "FETCH_FAILED"
    PARSE_FAILED = "PARSE_FAILED"
    CONFIG_MISMATCH = "CONFIG_MISMATCH"
    BLOCKED = "BLOCKED"
