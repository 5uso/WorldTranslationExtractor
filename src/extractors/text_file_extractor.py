from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

class TextFileExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.TEXT_FILE
    match_filenames = ()

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, text: list[str]) -> int:
        raise NotImplementedError