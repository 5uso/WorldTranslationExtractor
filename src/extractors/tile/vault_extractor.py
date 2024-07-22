from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.block_entity import BlockEntity

class VaultExtractor(TileExtractor):
    extractor_name = 'vault'
    match_tiles = ('vault',)
    data_version_range = (3953, 3953)

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        count += handle_item(tile.nbt['config']['key_item'], dictionary, self.item_extractors)

        if 'display_item' in tile.nbt['shared_data']:
            count += handle_item(tile.nbt['shared_data']['display_item'], dictionary, self.item_extractors)

        if 'items_to_eject' in tile.nbt['server_data']:
            for item in tile.nbt['server_data']['items_to_eject']:
                count += handle_item(item, dictionary, self.item_extractors)
        
        return count

extractor = VaultExtractor
