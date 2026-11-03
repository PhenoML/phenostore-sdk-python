from enum import StrEnum


class SearchTotalMode(StrEnum):
    ACCURATE = "accurate"
    ESTIMATE = "estimate"
    NONE = "none"

    def __str__(self) -> str:
        return str(self.value)
