from extractor_pass import ExtractorPass
from extract import list_extractors

from argparse import Namespace
from typing import Self
import itertools as it
import os

class InvalidSettingsException(Exception):
    def __init__(self, info: dict) -> None:
        self.info = info

        problems = []
        if 'missing_extractors' in info:
            problems.append(_('Extractors not found {}').format(info['missing_extractors']))
        if 'cannot_write' in info:
            problems.append(_('Could not write to file \'{}\'').format(info['cannot_write']))
        message = _("; ").join(problems)

        super().__init__(message)

def filter_extractors(extract: list[str], extractors: dict[ExtractorPass,list]) -> tuple[dict[ExtractorPass,list],list[str]]:
    return (
        {k: list(filter(lambda x: x.extractor_name in extract, extractors[k])) for k in ExtractorPass},
        list(set(extract) - set(it.chain(*((x.extractor_name for x in extractors[k]) for k in extractors))))
    )

class Settings:
    def __init__(self) -> None:
        self.extractors = {k: [] for k in ExtractorPass}
        self.out_lang = ''

    def from_args(args: Namespace) -> Self:
        s = Settings()
        info = dict()

        s.extractors = list_extractors()
        if args.extract:
            s.extractors, missing_extractors = filter_extractors(args.extract, s.extractors)
            if missing_extractors:
                info['missing_extractors'] = missing_extractors

        s.out_lang = args.lang
        if not os.access(s.out_lang, os.R_OK):
            info['cannot_write'] = s.out_lang

        if info:
            raise InvalidSettingsException(info)

        return s
