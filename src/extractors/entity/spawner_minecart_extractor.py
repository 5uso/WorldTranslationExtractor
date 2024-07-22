from extractors.entity_extractor import EntityExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from amulet.api.entity import Entity

class SpawnerMinecartExtractor(EntityExtractor):
    extractor_name = 'spawner_minecart'
    match_entities = ('spawner_minecart',)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        for potential in entity.nbt['SpawnPotentials']:
            namespace, base_name = str(potential['data']['entity']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, potential['data']['entity'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        if 'SpawnData' in entity.nbt:
            namespace, base_name = str(entity.nbt['SpawnData']['entity']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, entity.nbt['SpawnData']['entity'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        return count

extractor = SpawnerMinecartExtractor
