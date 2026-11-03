from enum import StrEnum


class BundleResourceType(StrEnum):
    BUNDLE = "Bundle"

    def __str__(self) -> str:
        return str(self.value)
