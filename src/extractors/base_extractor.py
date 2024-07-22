from extractor_pass import ExtractorPass
from dictionary import Dictionary
from settings import Settings
from util import Singleton

import abc

class BaseExtractor(metaclass=Singleton):
    extractor_pass = ExtractorPass.NONE
    data_version_range = (0, 0)

    def __init__(self, settings: Settings) -> None:
        pass

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, *args) -> int:
        raise NotImplementedError
