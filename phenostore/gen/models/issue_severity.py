from enum import StrEnum


class IssueSeverity(StrEnum):
    ERROR = "error"
    FATAL = "fatal"
    INFORMATION = "information"
    WARNING = "warning"

    def __str__(self) -> str:
        return str(self.value)
