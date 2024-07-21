from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

from amulet_nbt import NamedTag

class ItemExtractor(BaseExtractor):
    extractor_pass = ExtractorPass.ITEM
    match_items = ()

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, item: NamedTag) -> int:
        raise NotImplementedError
