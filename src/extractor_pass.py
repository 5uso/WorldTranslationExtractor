import enum

class ExtractorPass(enum.Enum):
    NONE = enum.auto()
    TILE = enum.auto()
    ENTITY = enum.auto()
