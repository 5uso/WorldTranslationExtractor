from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from collections import defaultdict

from amulet.api.block_entity import BlockEntity

class ContainerExtractor(TileExtractor):
    extractor_name = 'container'
    match_tiles = ('chest', 'furnace', 'shulker_box', 'barrel', 'smoker', 'blast_furnace', 'trapped_chest', 'hopper', 'dispenser', 'dropper', 'brewing_stand', 'campfire', 'chiseled_bookshelf', 'crafter')
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.indexes = defaultdict(lambda: 1)
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        if 'CustomName' in tile.nbt:
            tile.nbt['CustomName'], n = dictionary.replace_component(tile.nbt['CustomName'], f'container.{tile.base_name}.{self.indexes[tile.base_name]}.name')
            count += n

        if count:
            self.indexes[tile.base_name] += 1

        if 'Items' in tile.nbt:
            for item in tile.nbt['Items']:
                count += handle_item(item, dictionary, self.item_extractors)

        return count

extractor = ContainerExtractor
