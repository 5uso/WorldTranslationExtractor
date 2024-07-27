from extractors.item_extractor import ItemExtractor
from dictionary import Dictionary
from settings import Settings

from amulet_nbt import NamedTag, StringTag

class BookExtractor(ItemExtractor):
    extractor_name = 'book'
    match_items = ('written_book',)
    data_version_range = (3953, 3953)

    def __init__(self, settings: Settings) -> None:
        self.index = 1

    def extract(self, dictionary: Dictionary, item: NamedTag) -> int:
        if 'components' not in item or 'minecraft:written_book_content' not in item['components']:
            return 0

        count = 0

        if 'pages' in item['components']['minecraft:written_book_content']:
            for page in range(len(item['components']['minecraft:written_book_content']['pages'])):
                item['components']['minecraft:written_book_content']['pages'][page]['raw'], n = dictionary.replace_component(item['components']['minecraft:written_book_content']['pages'][page]['raw'], f'book.{self.index}.content.page{page}')
                count += n

        if 'title' in item['components']['minecraft:written_book_content'] and 'minecraft:custom_name' not in item['components']:
            key = dictionary.add_entry(str(item['components']['minecraft:written_book_content']['title']['raw']), f'book.{self.index}.title')
            item['components']['minecraft:custom_name'] = StringTag(f'{{"translate":"{key}","italic":false}}')
            count += 1

        if count:
            self.index += 1
        return count

extractor = BookExtractor
