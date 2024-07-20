from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

class BaseExtractor(metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.NONE

    def __init__(self, settings):
        pass

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, *args) -> int:
        raise NotImplementedError
