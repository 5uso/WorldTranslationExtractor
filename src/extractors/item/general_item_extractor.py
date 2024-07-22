from extractors.item_extractor import ItemExtractor
from extract import handle_entity, handle_tile
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from settings import Settings

from collections import defaultdict

from amulet_nbt import NamedTag

class GeneralItemExtractor(ItemExtractor):
    extractor_name = 'item'
    match_items = ('.*',)

    def __init__(self, settings: Settings) -> None:
        self.indexes = defaultdict(lambda: 1)
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]
        self.tile_extractors = [x(settings) for x in settings.extractors[ExtractorPass.TILE]]

    def extract(self, dictionary: Dictionary, item: NamedTag) -> int:
        count = 0

        # TODO: Amulet isn't compatible with 1.21 yet despite 0.10.33 claiming it is I guess
        print(item)

        if count:
            self.indexes[item['id']] += 1
        return count

extractor = GeneralItemExtractor
