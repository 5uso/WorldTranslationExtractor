from extractors.entity_extractor import EntityExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_item
from settings import Settings

from amulet.api.entity import Entity

class ItemEntityExtractor(EntityExtractor):
    extractor_name = 'item_entity'
    match_entities = {
        'ominous_item_spawner': ('item',),
        'trident': ('item',),
        'item_display': ('item',),
        'item_frame': ('Item',),
        'eye_of_ender': ('Item',),
        'item': ('Item',),
        'snowball': ('Item',),
        'small_fireball': ('Item',),
        'potion': ('Item',),
        'fireball': ('Item',),
        'experience_bottle': ('Item',),
        'ender_pearl': ('Item',),
        'egg': ('Item',),
        'firework_rocket': ('FireworksItem',),
        'zombie_horse': ('SaddleItem',),
        'skeleton_horse': ('SaddleItem',),
        'mule': ('SaddleItem',),
        'horse': ('SaddleItem',),
        'donkey': ('SaddleItem',),
        'arrow': ('item','weapon'),
        'spectral_arrow': ('item','weapon')
    }
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        for tag_name in self.match_entities[entity.base_name]:
            if tag_name in entity.nbt:
                count += handle_item(entity.nbt[tag_name], dictionary, self.item_extractors)
        
        return count

extactor = ItemEntityExtractor
