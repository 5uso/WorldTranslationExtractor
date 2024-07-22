from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity

class BeeExtractor(TileExtractor):
    extractor_name = 'bee'
    match_tiles = ('beehive', 'bee_nest')
    data_version_range = (2225, 3953)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        for bee in tile.nbt['bees']:
            namespace, base_name = str(bee['entity_data']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, bee['entity_data'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        return count

extractor = BeeExtractor
