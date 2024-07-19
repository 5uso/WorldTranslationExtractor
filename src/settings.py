from extractor_pass import ExtractorPass
from extract import list_extractors

from argparse import Namespace
from typing import Self
import itertools as it

class InvalidSettingsException(Exception):
    def __init__(self, info: dict) -> None:
        self.info = info
        super().__init__(_('Extractors not found {}').format(info['missing_extractors']))

def filter_extractors(extract: list[str], extractors: dict[ExtractorPass,list]) -> tuple[dict[ExtractorPass,list],list[str]]:
    return (
        {k: list(filter(lambda x: x.extractor_name in extract, extractors[k])) for k in ExtractorPass},
        list(set(extract) - set(it.chain(*((x.extractor_name for x in extractors[k]) for k in extractors))))
    )

class Settings:
    def __init__(self) -> None:
        self.extractors = {k: [] for k in ExtractorPass}

    def from_args(args: Namespace) -> Self:
        s = Settings()
        info = dict()

        s.extractors = list_extractors()
        if args.extract:
            s.extractors, info['missing_extractors'] = filter_extractors(args.extract, s.extractors)
            if info['missing_extractors']:
                raise InvalidSettingsException(info)

        return s
