from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.block_entity import BlockEntity

class ItemTileExtractor(TileExtractor):
    extractor_name = 'item_tile'
    match_tiles = {
        'jukebox': 'RecordItem',
        'lectern': 'Book',
        'decorated_pot': 'item'
    }
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        tag_name = self.match_tiles[tile.base_name]
        if tag_name in tile.nbt:
            count += handle_item(tile.nbt[tag_name], dictionary, self.item_extractors)
        
        return count

extractor = ItemTileExtractor
