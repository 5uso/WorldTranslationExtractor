from extractor_pass import ExtractorPass
import settings
import world
import abc

class BaseExtractor(metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.NONE

    @classmethod
    @abc.abstractmethod
    def extract(self, world: world.World, settings: settings.Settings) -> dict:
        raise NotImplementedError
