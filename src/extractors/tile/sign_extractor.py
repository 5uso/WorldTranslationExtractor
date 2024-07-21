from extractors.tile_extractor import TileExtractor
from dictionary import Dictionary
from settings import Settings

import itertools as it

from amulet.api.block_entity import BlockEntity

class SignExtractor(TileExtractor):
    extractor_name = 'sign'
    match_tiles = ('sign', 'hanging_sign')

    def __init__(self, settings: Settings) -> None:
        self.index = 1

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        for side, line in it.product(('front_text', 'back_text'), range(4)):
            tile.nbt[side]['messages'][line], n = dictionary.replace_component(tile.nbt[side]['messages'][line], f'sign.{self.index}.{side}.{line}')
            count += n

        if count:
            self.index += 1
        return count

extractor = SignExtractor
