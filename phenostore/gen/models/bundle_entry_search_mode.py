from enum import StrEnum


class BundleEntrySearchMode(StrEnum):
    INCLUDE = "include"
    MATCH = "match"

    def __str__(self) -> str:
        return str(self.value)
