from enum import StrEnum


class OperationOutcomeResourceType(StrEnum):
    OPERATIONOUTCOME = "OperationOutcome"

    def __str__(self) -> str:
        return str(self.value)
