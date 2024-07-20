from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
import abc

class TileExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.TILE
