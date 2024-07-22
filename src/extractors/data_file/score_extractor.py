from extractors.data_file_extractor import DataFileExtractor
from dictionary import Dictionary

from amulet_nbt import NamedTag

class ScoreExtractor(DataFileExtractor):
    extractor_name = 'score'
    match_filenames = ('scoreboard\.dat',)

    def extract(self, dictionary: Dictionary, data: NamedTag) -> int:
        count = 0

        for score in data['data']['Objectives']:
            score['DisplayName'], n = dictionary.replace_component(score['DisplayName'], f'score.{score["Name"]}.name')
            count += n

        for team in data['data']['Teams']:
            team['DisplayName'], n = dictionary.replace_component(team['DisplayName'], f'team.{team["Name"]}.name')
            team['MemberNamePrefix'], m = dictionary.replace_component(team['MemberNamePrefix'], f'team.{team["Name"]}.prefix')
            team['MemberNameSuffix'], l = dictionary.replace_component(team['MemberNameSuffix'], f'team.{team["Name"]}.suffix')
            count += n + m + l

        return count

extractor = ScoreExtractor
