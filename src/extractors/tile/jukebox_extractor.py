from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.block_entity import BlockEntity

class JukeboxExtractor(TileExtractor):
    extractor_name = 'jukebox'
    match_tiles = ('jukebox')

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        if 'RecordItem' in tile.nbt:
            count += handle_item(tile.nbt['RecordItem'], dictionary, self.item_extractors)
        
        return count

extractor = JukeboxExtractor
