from enum import StrEnum


class SearchSummaryMode(StrEnum):
    COUNT = "count"
    DATA = "data"
    FALSE = "false"
    TEXT = "text"
    TRUE = "true"

    def __str__(self) -> str:
        return str(self.value)
