from extractors.data_file_extractor import DataFileExtractor
from dictionary import Dictionary

from amulet_nbt import NamedTag, CompoundTag, ListTag, StringTag

class StorageExtractor(DataFileExtractor):
    extractor_name = 'storage'
    match_filenames = ('command_storage_.*\.dat',)

    def extract(self, dictionary: Dictionary, data: NamedTag) -> int:
        count = 0

        for storage_name in data['data']['contents']:
            stack = [data['data']['contents'][storage_name]]
            while stack:
                tag = stack.pop()
                if isinstance(tag, CompoundTag):
                    for name in tag:
                        if isinstance(tag[name], StringTag):
                            tag[name], n = dictionary.replace_component(tag[name], f'storage.{storage_name}')
                            count += n
                            continue
                        stack.append(tag[name])
                    continue
                if isinstance(tag, ListTag):
                    for i in range(len(tag)):
                        if isinstance(tag[i], StringTag):
                            tag[i], n = dictionary.replace_component(tag[i], f'storage.{storage_name}')
                            count += n
                            continue
                        stack.append(tag[i])

        return count

extractor = StorageExtractor
