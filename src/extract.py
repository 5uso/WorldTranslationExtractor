from extractor_pass import ExtractorPass
from dictionary import Dictionary
from world import World

from glob import glob
from tqdm import tqdm
import os

from amulet.api.data_types import VersionIdentifierType, Dimension, ChunkCoordinates
from amulet.api.chunk.entity_list import EntityList
from amulet.api.block_entity import BlockEntity
from amulet.api.level.world import World
from amulet.api.entity import Entity
from amulet.api.chunk import Chunk

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

def handle_tile(tile: BlockEntity, dictionary: Dictionary) -> int:
    return 0

def handle_chunk(chunk: Chunk, dictionary: Dictionary) -> None:
    for block_entity in chunk.block_entities:
        chunk.changed |= bool(handle_tile(block_entity, dictionary))

def handle_entity(entity: Entity, dictionary: Dictionary) -> int:
    return 0

def handle_entities(entities: tuple[EntityList,VersionIdentifierType], level: World, coord: ChunkCoordinates, dimension: Dimension, dictionary: Dictionary) -> None:
    entities = entities[0]
    changed = False
    for e in entities:
        changed |= bool(handle_entity(e, dictionary))
    if changed:
        level.set_native_entites(*coord, dimension, entities)

def handle_chunks(world: World, settings: 'Settings', dictionary: Dictionary) -> None:
    for dimension in world.level.dimensions:
        if settings.dimensions and dimension not in settings.dimensions:
            continue
        
        chunk_coords = sorted(world.level.all_chunk_coords(dimension))
        if not chunk_coords:
            continue

        print(_('Scanning dimension \'{}\'...').format(dimension))
        for i, coord in enumerate(tqdm(chunk_coords, unit = "chunk")):
            handle_chunk(world.level.get_chunk(*coord, dimension), dictionary)
            handle_entities(world.level.get_native_entities(*coord, dimension), world.level, coord, dimension, dictionary)

            if not (i + 1) % settings.batch:
                print()
                world.level.save()
                world.level.unload()
        world.level.save()
        world.level.unload()
    world.level.close()

def extract(world: World, settings: 'Settings') -> None:
    dictionary = Dictionary(settings)

    handle_chunks(world, settings, dictionary)
