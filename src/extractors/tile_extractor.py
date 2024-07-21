from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

from amulet.api.block_entity import BlockEntity

class TileExtractor(BaseExtractor):
    extractor_pass = ExtractorPass.TILE
    match_tiles = ()

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        raise NotImplementedError
