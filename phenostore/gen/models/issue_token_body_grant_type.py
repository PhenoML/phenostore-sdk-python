from enum import StrEnum


class IssueTokenBodyGrantType(StrEnum):
    CLIENT_CREDENTIALS = "client_credentials"

    def __str__(self) -> str:
        return str(self.value)
