from extractors.data_file_extractor import DataFileExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary
from extract import handle_entity
from settings import Settings

from amulet.api.entity import Entity
from amulet_nbt import NamedTag

class LevelExtractor(DataFileExtractor):
    extractor_name = 'level'
    match_filenames = ('level\.dat',)
    data_version_range = (169, 3953)

    def __init__(self, settings: Settings) -> None:
        self.entity_extractors = [x(settings) for x in settings.extractors[ExtractorPass.ENTITY]]

    def extract(self, dictionary: Dictionary, data: NamedTag) -> int:
        count = 0

        if 'Player' in data['Data']:
            entity = Entity("minecraft", "player", 0.0, 0.0, 0.0, data['Data']['Player'])
            count += handle_entity(entity, dictionary, self.entity_extractors)

        if 'CustomBossEvents' in data['Data']:
            for bossbar in data['Data']['CustomBossEvents']:
                data['Data']['CustomBossEvents'][bossbar]['Name'], n = dictionary.replace_component(data['Data']['CustomBossEvents'][bossbar]['Name'], f'bossbar.{bossbar}.name')
                count += n

        return count

extractor = LevelExtractor
