from extractors.entity_extractor import EntityExtractor
from dictionary import Dictionary
from settings import Settings

from amulet.api.entity import Entity

class TextDisplayExtractor(EntityExtractor):
    extractor_name = 'text_display'
    match_entities = ('text_display',)
    data_version_range = (3337, 3953)

    def __init__(self, settings: Settings) -> None:
        self.index = 1

    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        count = 0

        if 'text' in entity.nbt:
            entity.nbt['text'], n = dictionary.replace_component(entity.nbt['text'], f'text_display.{self.index}.text')
            count += n

        if count:
            self.index += 1
        return count

extactor = TextDisplayExtractor
