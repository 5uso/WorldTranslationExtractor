import enum

class ExtractorPass(enum.Enum):
    NONE = enum.auto()
    CHUNK = enum.auto()
    ENTITY = enum.auto()
