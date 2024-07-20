from extractors.tile_extractor import TileExtractor
from dictionary import Dictionary

from amulet.api.block_entity import BlockEntity

class TestExtractor(TileExtractor):
    extractor_name = 'test'
    match_tiles = ('chest',)

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        print(tile)
        return 0

extractor = TestExtractor
