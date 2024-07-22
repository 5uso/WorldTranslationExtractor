from extractor_pass import ExtractorPass
from extract import list_extractors

from argparse import Namespace
from typing import Self
import itertools as it

class InvalidSettingsException(Exception):
    def __init__(self, info: dict) -> None:
        self.info = info

        problems = []
        if 'missing_extractors' in info:
            problems.append(_('Extractors not found {}').format(info['missing_extractors']))
        if 'incompatible_extractors' in info:
            problems.append(_('Extractors incompatible with data version {}').format(info['incompatible_extractors']))
        if 'cannot_write' in info:
            problems.append(_('Could not write to file \'{}\'').format(info['cannot_write']))
        message = _("; ").join(problems) + '.'

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
        self.dimensions = []
        self.keepdup = False
        self.sort = False
        self.batch = 0
        self.indent = 0
        self.data_version = 0
        self.versionless = False

    def from_args(args: Namespace, data_version: int) -> Self:
        s = Settings()
        info = dict()

        s.extractors = list_extractors()
        if args.extract:
            s.extractors, missing_extractors = filter_extractors(args.extract, s.extractors, data_version)
            if missing_extractors:
                info['missing_extractors'] = missing_extractors

        s.out_lang = args.lang
        try:
            with open(s.out_lang, 'w') as f:
                if not f.writable():
                    raise Exception
        except Exception:
            info['cannot_write'] = s.out_lang

        s.dimensions = [d if ':' in d else f'minecraft:{d}' for d in args.dimension] if args.dimension else []
        s.keepdup = args.keepdup
        s.sort = args.sort
        s.batch = args.batch
        s.indent = args.indent
        s.data_version = data_version
        s.versionless = args.versionless

        if not s.versionless:
            incompatible_extractors = []
            for extractor_pass in s.extractors:
                for extractor in s.extractors[extractor_pass]:
                    if extractor.data_version_range[0] > s.data_version or extractor.data_version_range[1] < s.data_version:
                        incompatible_extractors.append(extractor.extractor_name)
            if incompatible_extractors:
                info['incompatible_extractors'] = incompatible_extractors

        if info:
            raise InvalidSettingsException(info)

        return s
