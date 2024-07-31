from extractors.tile_extractor import TileExtractor
from dictionary import Dictionary
from settings import Settings

from amulet.api.block_entity import BlockEntity
from amulet_nbt import StringTag

class CommandBlockExtractor(TileExtractor):
    extractor_name = 'command_block'
    match_tiles = ('command_block',)
    data_version_range = (819, 3953)

    def __init__(self, settings: Settings) -> None:
        self.index = 1

    def extract(self, dictionary: Dictionary, tile: BlockEntity) -> int:
        cmd, count = dictionary.replace_command(str(tile.nbt['Command']), f'command_block.{self.index}.command')
        tile.nbt['Command'] = StringTag(cmd)

        if count:
            self.index += 1
        return count

extractor = CommandBlockExtractor
