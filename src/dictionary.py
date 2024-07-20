from typing import TYPE_CHECKING
if TYPE_CHECKING: from settings import Settings

class Dictionary():
    def __init__(self, settings: "Settings") -> None:
        self.keepdup = settings.keepdup
        self.data = dict()
