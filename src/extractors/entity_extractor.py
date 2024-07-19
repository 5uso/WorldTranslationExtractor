from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
import abc

class EntityExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.ENTITY
