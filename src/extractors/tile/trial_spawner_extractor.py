from extractors.tile_extractor import TileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity

class TrialSpawnerExtractor(TileExtractor):
    extractor_name = 'trial_spawner'
    match_tiles = ('trial_spawner',)
    data_version_range = (3953, 3953)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        count = 0

        for config in ('normal_config', 'ominous_config'):
            if config not in tile.nbt:
                continue

            # For some insane reason spawn_potentials and spawn_data in 1.21 are inconsistent with mob_spawner nbt
            for potential in tile.nbt[config]['spawn_potentials']:
                namespace, base_name = str(potential['data']['entity']['id']).split(':')
                entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, potential['data']['entity'])
                count += handle_entity(entity, dictionary, self.entity_extractors)

        if 'spawn_data' in tile.nbt:
            namespace, base_name = str(tile.nbt['spawn_data']['entity']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, tile.nbt['spawn_data']['entity'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        return count

extractor = TrialSpawnerExtractor
