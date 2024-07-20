from extractor_pass import ExtractorPass
from world import World

from glob import glob
from tqdm import tqdm
import os

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

def extract(world: World, settings: 'Settings') -> None:
    for dimension in world.level.dimensions:
        if settings.dimensions and dimension not in settings.dimensions:
            continue
        
        chunk_coords = sorted(world.level.all_chunk_coords(dimension))
        if not chunk_coords:
            continue

        print(_('Scanning dimension \'{}\'...').format(dimension))
        for i, coord in enumerate(tqdm(chunk_coords, unit = "chunk")):
            chunk = world.level.get_chunk(*coord, dimension)
            entities = world.level.get_native_entities(*coord, dimension)

            if not (i + 1) % settings.batch:
                print()
                world.level.save()
                world.level.unload()
        world.level.save()
        world.level.unload()
    world.level.close()