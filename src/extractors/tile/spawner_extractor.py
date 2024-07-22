from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity

class SpawnerExtractor(TileExtractor):
    extractor_name = 'spawner'
    match_tiles = ('mob_spawner',)
    data_version_range = (2860, 3953)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        for potential in tile.nbt['SpawnPotentials']:
            namespace, base_name = str(potential['data']['entity']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, potential['data']['entity'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        if 'SpawnData' in tile.nbt:
            namespace, base_name = str(tile.nbt['SpawnData']['entity']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, tile.nbt['SpawnData']['entity'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        return count

extractor = SpawnerExtractor
