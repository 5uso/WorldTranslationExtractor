from extractor_pass import ExtractorPass
from dictionary import Dictionary
import settings
import world
import abc

class BaseExtractor(metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.NONE

    @classmethod
    @abc.abstractmethod
    def extract(self, world: world.World, settings: settings.Settings, dictionary: Dictionary) -> None:
        raise NotImplementedError
