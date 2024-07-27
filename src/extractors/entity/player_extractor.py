from extractors.entity_extractor import EntityExtractor
from extract import handle_entity, handle_item
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from settings import Settings

from amulet.api.entity import Entity

class PlayerExtractor(EntityExtractor):
    extractor_name = 'player'
    match_entities = ('player',)
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        if 'EnderItems' in entity.nbt:
            for item in entity.nbt['EnderItems']:
                count += handle_item(item, dictionary, self.item_extractors)

        for entity_slot in ('ShoulderEntityLeft', 'ShoulderEntityRight'):
            if entity_slot in entity.nbt:
                namespace, base_name = str(entity.nbt[entity_slot]['id']).split(':')
                inner_entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, entity.nbt[entity_slot])
                count += handle_entity(inner_entity, dictionary, self.entity_extractors)

        return count

extractor = PlayerExtractor
