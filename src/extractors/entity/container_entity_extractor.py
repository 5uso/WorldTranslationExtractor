from extractors.entity_extractor import EntityExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.entity import Entity

class ContainerEntityExtractor(EntityExtractor):
    extractor_name = 'container_entity'
    match_entities = {
        'hopper_minecart': 'Items',
        'chest_minecart': 'Items',
        'chest_boat': 'Items',
        'trader_llama': 'Items',
        'mule': 'Items',
        'llama': 'Items',
        'donkey': 'Items',
        'wandering_trader': 'Inventory',
        'villager': 'Inventory',
        'pillager': 'Inventory',
        'player': 'Inventory',
        'piglin': 'Inventory',
        'allay': 'Inventory'
    }
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        tag_name = self.match_entities[entity.base_name]
        if tag_name in entity.nbt:
            for item in entity.nbt[tag_name]:
                count += handle_item(item, dictionary, self.item_extractors)
        
        return count

extractor = ContainerEntityExtractor
