from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

from amulet_nbt import NamedTag

class DataFileExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.DATA_FILE
    match_filenames = ()

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, data: NamedTag) -> int:
        raise NotImplementedError
