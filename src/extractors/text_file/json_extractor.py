from extractors.text_file_extractor import TextFileExtractor
from dictionary import Dictionary

class JsonExtractor(TextFileExtractor):
    extractor_name = 'json'
    match_filenames = ('.*\.json',)
    data_version_range = (1519, 2147483647)

    def extract(self, dictionary: Dictionary, file: tuple[list[str],list[str]]) -> int:
        count = 0
        path, contents = file
        key_path = ".".join(path)

        for line in range(len(contents)):
            contents[line], n = dictionary.replace_other(contents[line], f'json.{key_path}.line{line}')
            count += n

        return count

extractor = JsonExtractor
