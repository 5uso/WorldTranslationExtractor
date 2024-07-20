from extractors.base_extractor import BaseExtractor
from extractor_pass import ExtractorPass
from dictionary import Dictionary

import abc

from amulet.api.entity import Entity

class EntityExtractor(BaseExtractor, metaclass=abc.ABCMeta):
    extractor_pass = ExtractorPass.ENTITY
    match_entities = ()

    @classmethod
    @abc.abstractmethod
    def extract(self, dictionary: Dictionary, entity: Entity) -> int:
        raise NotImplementedError
