from extractors.entity_extractor import EntityExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.entity import Entity

class MobExtractor(EntityExtractor):
    extractor_name = 'mob'
    match_entities = ('.*',) # Not all entities are mobs, but for future proofing it's better to assume they are
    data_version_range = (169, 3953)

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        if 'ArmorItems' in entity.nbt:
            for item in entity.nbt['ArmorItems']:
                count += handle_item(item, dictionary, self.item_extractors)

        if 'HandItems' in entity.nbt:
            for item in entity.nbt['HandItems']:
                count += handle_item(item, dictionary, self.item_extractors)

        if 'body_armor_item' in entity.nbt:
            count += handle_item(entity.nbt['body_armor_item'], dictionary, self.item_extractors)

        return count

extractor = MobExtractor
