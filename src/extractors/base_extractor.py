import world

class BaseExtractor():
    def __init__(self) -> None:
        pass

    def extract(self, world: world.World) -> dict:
        raise NotImplementedError
