from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
import abc

class ChunkExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.CHUNK
