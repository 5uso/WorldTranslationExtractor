from extractor_pass import ExtractorPass
from dictionary import Dictionary
from world import World

import itertools as it
from glob import glob
from tqdm import tqdm
import json
import os

from amulet.api.data_types import VersionIdentifierType, Dimension, ChunkCoordinates
from amulet.api.chunk.entity_list import EntityList
from amulet.api.level.world import World as Level
from amulet.api.block_entity import BlockEntity
from amulet.api.entity import Entity
from amulet.api.chunk import Chunk
import amulet_nbt as nbt

from typing import TYPE_CHECKING
if TYPE_CHECKING: from settings import Settings # Why must python torture me like this

def list_extractors() -> dict[ExtractorPass,list]:
    extractors = {k: [] for k in ExtractorPass}

    for f in glob('src/extractors/*.py'):
        name = os.path.splitext(os.path.basename(f))[0]
        module = getattr(__import__('extractors.' + name), name)
        if hasattr(module, 'extractor'):
            extractors[module.extractor.extractor_pass].append(module.extractor)
        
    return extractors

def handle_tile(tile: BlockEntity, dictionary: Dictionary, extractors: list) -> int:
    return sum(extractor.extract(dictionary, tile) for extractor in extractors if tile.base_name in extractor.match_tiles)

def handle_chunk(chunk: Chunk, dictionary: Dictionary, extractors: list) -> None:
    chunk.changed = not all(not bool(handle_tile(block_entity, dictionary, extractors)) for block_entity in chunk.block_entities)

def handle_entity(entity: Entity, dictionary: Dictionary, extractors: list) -> int:
    return sum(extractor.extract(dictionary, entity) for extractor in extractors if entity.base_name in extractor.match_entities)

def handle_entities(entities: tuple[EntityList,VersionIdentifierType], level: Level, coord: ChunkCoordinates, dimension: Dimension, dictionary: Dictionary, extractors: list) -> None:
    entities = entities[0]
    changed = not all(not bool(handle_entity(entity, dictionary, extractors)) for entity in entities)
    if changed:
        level.set_native_entites(*coord, dimension, entities)

def handle_chunks(world: World, settings: 'Settings', dictionary: Dictionary, extractors: dict[ExtractorPass,list]) -> None:
    for dimension in world.level.dimensions:
        if settings.dimensions and dimension not in settings.dimensions:
            continue
        
        chunk_coords = sorted(world.level.all_chunk_coords(dimension))
        if not chunk_coords:
            continue

        print(_('Scanning dimension \'{}\'...').format(dimension))
        for i, coord in enumerate(tqdm(chunk_coords, unit = "chunk")):
            handle_chunk(world.level.get_chunk(*coord, dimension), dictionary, extractors[ExtractorPass.TILE])
            handle_entities(world.level.get_native_entities(*coord, dimension), world.level, coord, dimension, dictionary, extractors[ExtractorPass.ENTITY])

            if not (i + 1) % settings.batch:
                print()
                world.level.save()
                world.level.unload()
        world.level.save()
        world.level.unload()
    world.level.close()

def handle_structures(path: str, dictionary: Dictionary, extractors: dict[ExtractorPass,list]) -> None:
    for f in it.chain(
        glob(path + '/generated/*/structures/**/*.nbt', recursive=True),
        glob(path + '/datapacks/*/data/*/structures/**/*.nbt', recursive=True)
    ):
        structure = nbt.load(f)
        if 'blocks' in structure.tag:
            for block_tag in filter(lambda x: 'nbt' in x, structure.tag['blocks']):
                namespace, base_name = str(block_tag['nbt']['id']).split(':')
                x, y, z = (int(p) for p in block_tag['pos'])
                tile = BlockEntity(namespace, base_name, x, y, z, block_tag['nbt'])
                handle_tile(tile, dictionary, extractors[ExtractorPass.TILE])

        if 'entities' in structure.tag:
            for entity_tag in filter(lambda x: 'nbt' in x, structure.tag['entities']):
                namespace, base_name = str(entity_tag['nbt']['id']).split(':')
                x, y, z = (float(p) for p in entity_tag['pos'])
                entity = Entity(namespace, base_name, x, y, z, entity_tag['nbt'])
                handle_entity(entity, dictionary, extractors[ExtractorPass.ENTITY])              

        structure.save_to(f)

def extract(world: World, settings: 'Settings') -> None:
    dictionary = Dictionary(settings)
    extractors = {k: [x(settings) for x in settings.extractors[k]] for k in settings.extractors}

    handle_chunks(world, settings, dictionary, extractors)
    handle_structures(world.path, dictionary, extractors)

    print(_('Outputting lang to \'{}\'...').format(settings.out_lang))
    lang = dictionary.reverse()
    with open(settings.out_lang, 'w') as f:
        json.dump(lang, f, indent=settings.indent, sort_keys=settings.sort)
