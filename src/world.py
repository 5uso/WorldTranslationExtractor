import amulet_nbt
import amulet

class WorldLoadException(Exception):
    def __init__(self, cause: Exception) -> None:
        self.cause = cause
        super().__init__(cause)

class World():
    def __init__(self, path: str) -> None:
        self.path = path
        self.level = amulet.load_level(path)
        self.data_version = int(amulet_nbt.load(path + '/level.dat')['Data']['DataVersion'])

def try_load_world(path: str) -> World:
    try:
        w = World(path)
    except Exception as e:
        raise WorldLoadException(e)

    return w
