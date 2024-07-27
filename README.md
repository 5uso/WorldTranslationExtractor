# WorldTranslationExtractor
 
A tool to extract translatable text from Minecraft worlds to facilitate localization.

Read this file in other languages: [ES](./language/es/README.md)

## Basics

Scans a whole save and associated files, finding json text components (as well as plain text where applicable) and replacing them with translate json components.

Currently supports Minecraft Java Edition 1.21. The code that manages NBT structures is modular, which means that different extractors may be defined for different Minecraft versions and loaded dynamically.

Depends on the [Amulet world editor](https://www.amuletmc.com/) API.

## Usage
World Translation Extractor currently provides a command line interface.
```
python3 main.py [-h] --world WORLD [--out OUT] [--force | -f]
                                   [--lang LANG] [--extract EXTRACT] [--dimension DIMENSION]
                                   [--keepdup | -k] [--sort | -s]
                                   [--indent INDENT] [--batch BATCH]
                                   [--versionless | -v]
options:
  -h, --help            show this help message and exit
  --world WORLD, -w WORLD
                        Path to the target world.
  --out OUT, -o OUT     Path to output a translated copy of the world. By default, outputs to
                        <WORLD>_wte.
  --force, --no-force, -f
                        Delete previous contents of <OUT> before extracting.
  --lang LANG, -l LANG  Path to output translation json. By default, outputs to wte_lang.json.
  --extract EXTRACT, -e EXTRACT
                        An extractor to run over the world, multiple may be selected. If no
                        extractors are specified, all available extractors will be run.
  --dimension DIMENSION, -d DIMENSION
                        A dimension to scan, multiple may be selected. If no dimensions are
                        specified, all dimensions will be scanned.
  --keepdup, --no-keepdup, -k
                        Keep duplicate translation texts as separate keys.
  --sort, --no-sort, -s
                        Sort output json alphabetically.
  --indent INDENT, -i INDENT
                        Amount of spaces used to indent the output json.
  --batch BATCH, -b BATCH
                        When iterating the world, save every <BATCH> chunks.
  --versionless, --no-versionless, -v
                        Ignore extractor data version incompatibilities.
```
For example, `python3 main.py -w "C:\Users\el sus\AppData\Roaming\.minecraft\saves\WTE_Test"` would extract translations from a world named WTE_Test using default settings.

The world is copied to a new folder in the same directory as the original. A json file containing the extracted strings, associated to translation keys, is created in the working directory. This file is formatted just as resourcepack lang files.

## Installation
Runs on [Python](https://www.python.org/downloads/) 3.9+ (3.11+ recommended). IF you're running Windows, it may be convenient to install python through the Microsoft Store.

Download or clone this repo, then install the required dependencies with `python3 -m pip install -r requirements.txt` .

## Extractors
The following extractor modules are included in this repository. They all work in Minecraft 1.21, some of them support older DataVersions. Check their source files for more details.
### Tile extractors
Tile extractors run over all tile entities in the world, as well as any found within structure files in datapacks or the generated folder.
#### `bee`
Manages `beehive` and `bee_nest`. Extracts entities from the `bees` tag.
#### `command_block`
Manages `command_block`. Extracts components from the `Command` field.
#### `container`
Manages the following containers: `'chest', 'furnace', 'shulker_box', 'barrel', 'smoker', 'blast_furnace', 'trapped_chest', 'hopper', 'dispenser', 'dropper', 'brewing_stand', 'campfire', 'chiseled_bookshelf', 'crafter'`. Extracts their `CustomName`, as well as any `Items` within them.
#### `item_tile`
Extracts `RecordItem` from `jukebox`, `Book` from `lectern`, and `item` from `decorated_pot`.
#### `sign`
Manages both `sign` and `hanging_sign`. Extracts `messages` from `front_text` and `back_text`.
#### `spawner`
Manages `mob_spawner`. Extracts entities from `SpawnData` and `SpawnPotentials`.
#### `trial_spawner`
Manages `trial_spawner`. Extracts entities from `spawn_data`, and from `spawn_potentials` both for `normal_config` and `ominous_config`.
#### `vault`
Manages `vault`. Extracts items from `key_item`, `display_item`, and `items_to_eject`.
### Entity extractors
Entity extractors run over all entities in the world, as well as any found within structure files in datapacks or the generated folder.
#### `command_block_minecart`
Manages `command_block_minecart`. Extracts components from the `Command` field.
#### `container_entity`
Extracts `Items` from `'hopper_minecart', 'chest_minecart', 'chest_boat', 'trader_llama', 'mule', 'llama', 'donkey'`; and `Inventory` from `'wandering_trader', 'villager', 'pillager', 'player', 'piglin', 'allay'`.
#### `entity`
Runs for all entities. Extracts `CustomName`, and other entities from `Passengers`.
#### `item_entity`
Extracts `item` from `'arrow', 'spectral_arrow', 'ominous_item_spawner', 'trident', 'item_display'`; `Item` from `'item_frame', 'eye_of_ender', 'item', 'snowball', 'small_fireball', 'potion', 'fireball', 'experience_bottle', 'ender_pearl', 'egg'`; `FireworksItem` from `'firework_rocket'`; `SaddleItem` from `'zombie_horse', 'skeleton_horse', 'mule', 'horse', 'donkey'`; and `weapon` from `'arrow', 'spectral_arrow'`.
#### `mob`
Runs for all entities (for future proofing). Extracts items from `ArmorItems`, `HandItems`, and `body_armor_item`.
#### `player`
Manages `player`. Extracts items from `EnterItems`, and entities from `ShoulderEntityLeft` and `ShoulderEntityRight`.
#### `spawner_minecart`
Manages `spawner_minecart`. Extracts entities from `SpawnData` and `SpawnPotentials`.
#### `text_display`
Manages `text_display`. Extracts `text`.
#### `villager`
Manages `villager`, `zombie_villager`, and `wandering_trader`. Extracts items from `Offers`.
### Item extractors
Item extractors run over all items found within entities, block entities, or other items.
#### `book`
Manages `written_book`. Extracts text from `pages` and `title`. The title translation is set as the item's custom name if no other exists. `author` is omitted. This comes as a result of `title` and `author` not supporting json components.
#### `item`
Runs for all items. Extracts `custom_name`, `item_name`, and `lore`; as well as tiles from `block_entity_data`, items from `container`, and entities from `entity_data`.
### Data file extractors
Data file extractors target specific dat files in the save folder.
#### `level`
Manages `level.dat`. Extracts the `Player`, as well as bossbar titles from `CustomBossEvents`.
#### `score`
Manages `scoreboard.dat`. Extracts scoreboard objective names from `Objectives`; and team names, prefixes, and suffixes from `Teams`.
#### `storage`
Manages all command storage dat files. Iterates all possible components recursively, replacing only instances using json text components.
### Text file extractors
Text file extractors target plain text files included in datapacks.
#### `function`
Manages all datapack mcfunction files. Extracts any found text component, as well as plain text matches in the `bossbar` command.
#### `json`
Manages all datapack json files. Extracts any found text component.

## Crediting
Explicit crediting within projects using this tool isn't required, but still appreciated.

## Contributing
Contributions, especially in the form of new extractors or extractor updates to new Minecraft versions, are welcome.

This tool itself can also be translated (via the `language` folder). Translations to other languages are appreciated!
