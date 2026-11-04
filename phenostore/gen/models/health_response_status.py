from enum import StrEnum


class HealthResponseStatus(StrEnum):
    OK = "ok"

    def __str__(self) -> str:
        return str(self.value)
