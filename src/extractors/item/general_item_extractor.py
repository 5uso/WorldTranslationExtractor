from extractors.item_extractor import ItemExtractor
from extract import handle_entity, handle_tile, handle_item
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from settings import Settings

from collections import defaultdict

from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity
from amulet_nbt import NamedTag

class GeneralItemExtractor(ItemExtractor):
    extractor_name = 'item'
    match_items = ('.*',)
    data_version_range = (3953, 3953)

    def __init__(self, settings: Settings) -> None:
        self.indexes = defaultdict(lambda: 1)
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]
        self.tile_extractors = [x(settings) for x in settings.extractors[ExtractorPass.TILE]]
        self.item_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ITEM]]

    def extract(self, dictionary: Dictionary, item: NamedTag) -> int:
        if 'components' not in item:
            return 0

        count = 0
        namespace, base_name = str(item['id']).split(':')

        if 'minecraft:custom_name' in item['components']:
            item['components']['minecraft:custom_name'], n = dictionary.replace_component(item['components']['minecraft:custom_name'], f'item.{base_name}.{self.indexes[base_name]}.name')
            count += n

        if 'minecraft:item_name' in item['components']:
            item['components']['minecraft:item_name'], n = dictionary.replace_component(item['components']['minecraft:item_name'], f'item.{base_name}.{self.indexes[base_name]}.item_name')
            count += n

        if 'minecraft:lore' in item['components']:
            for line in range(len(item['components']['minecraft:lore'])):
                item['components']['minecraft:lore'][line], n = dictionary.replace_component(item['components']['minecraft:lore'][line], f'item.{base_name}.{self.indexes[base_name]}.lore.line{line}')
                count += n

        if count:
            self.indexes[base_name] += 1

        if 'minecraft:block_entity_data' in item['components']:
            namespace, base_name = str(item['components']['minecraft:block_entity_data']['id']).split(':')
            tile = BlockEntity(namespace, base_name, 0, 0, 0, item['components']['minecraft:block_entity_data'])
            count += handle_tile(tile, dictionary, self.tile_extractors)

        if 'minecraft:container' in item['components']: # What the fuck????
            for useless_wrapper_that_only_helps_make_the_format_inconsistent_with_actual_containers in item['components']['minecraft:container']:
                inner_item = useless_wrapper_that_only_helps_make_the_format_inconsistent_with_actual_containers['item']
                count += handle_item(inner_item, dictionary, self.item_extractors)

        if 'minecraft:entity_data' in item['components']:
            namespace, base_name = str(item['components']['minecraft:entity_data']['id']).split(':')
            entity = Entity(namespace, base_name, 0.0, 0.0, 0.0, item['components']['minecraft:entity_data'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        return count

extractor = GeneralItemExtractor
