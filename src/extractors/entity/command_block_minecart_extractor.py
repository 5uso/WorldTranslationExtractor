from extractors.entity_extractor import EntityExtractor
from dictionary import Dictionary
from settings import Settings

from amulet.api.entity import Entity
from amulet_nbt import StringTag

class CommandBlockMinecartExtractor(EntityExtractor):
    extractor_name = 'command_block_minecart'
    match_entities = ('command_block_minecart',)
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.index = 1

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        cmd, count = dictionary.replace_command(entity.nbt['Command'], f'command_block_minecart.{self.index}.command')
        entity.nbt['Command'] = StringTag(cmd)

        if count:
            self.index += 1
        return count

extractor = CommandBlockMinecartExtractor
