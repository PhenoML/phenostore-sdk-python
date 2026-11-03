from enum import StrEnum


class BulkOperationAcceptedStatus(StrEnum):
    PENDING = "pending"

    def __str__(self) -> str:
        return str(self.value)
