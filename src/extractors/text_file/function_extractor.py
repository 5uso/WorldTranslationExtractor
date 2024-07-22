from extractors.text_file_extractor import TextFileExtractor
from dictionary import Dictionary

class FunctionExtractor(TextFileExtractor):
    extractor_name = 'function'
    match_filenames = ('.*\.mcfunction',)
    data_version_range = (1519, 2147483647)

    def extract(self, dictionary: Dictionary, file: tuple[list[str],list[str]]) -> int:
        count = 0
        path, contents = file
        key_path = ".".join(path)

        for cmd in range(len(contents)):
            contents[cmd], n = dictionary.replace_command(contents[cmd], f'function.{key_path}.line{cmd}')
            count += n

        return count

extractor = FunctionExtractor
