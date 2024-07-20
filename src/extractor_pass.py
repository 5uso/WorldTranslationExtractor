import enum

class ExtractorPass(enum.Enum):
    NONE = enum.auto()
    TILE = enum.auto()
    ENTITY = enum.auto()
    DATA_FILE = enum.auto()
    TEXT_FILE = enum.auto()
