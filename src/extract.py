from extractor_pass import ExtractorPass
from world import World

from glob import glob
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

def extract(world: World, settings: 'Settings'):
    pass
