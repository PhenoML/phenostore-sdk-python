from enum import StrEnum


class BundleType(StrEnum):
    BATCH_RESPONSE = "batch-response"
    HISTORY = "history"
    SEARCHSET = "searchset"
    TRANSACTION_RESPONSE = "transaction-response"

    def __str__(self) -> str:
        return str(self.value)
