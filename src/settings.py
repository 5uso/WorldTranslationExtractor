from typing import Self

class InvalidSettingsException(Exception):
    def __init__(self) -> None:
        super().__init__()

class Settings:
    def __init__(self) -> None:
        pass

    def from_args(args: dict) -> Self:
        return Settings()
