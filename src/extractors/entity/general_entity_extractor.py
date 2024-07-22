from extractors.entity_extractor import EntityExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from collections import defaultdict

from amulet.api.entity import Entity

class GeneralEntityExtractor(EntityExtractor):
    extractor_name = 'entity'
    match_entities = ('.*',)

    def __init__(self, settings: Settings) -> None:
        self.indexes = defaultdict(lambda: 1)
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        if 'CustomName' in entity.nbt:
            entity.nbt['CustomName'], n = dictionary.replace_component(entity.nbt['CustomName'], f'entity.{entity.base_name}.{self.indexes[entity.base_name]}.name')
            count += n

        if 'Passengers' in entity.nbt:
            for passenger in entity.nbt['Passengers']:
                namespace, base_name = str(passenger['id']).split(':')
                entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, passenger)
                count += handle_entity(entity, dictionary, self.entity_extractors)

        if count:
            self.indexes[entity.base_name] += 1
        return count

extactor = GeneralEntityExtractor
