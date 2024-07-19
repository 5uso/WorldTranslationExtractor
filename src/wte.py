import settings
import extract
import world

import argparse
import enum

class ExitCode(enum.IntEnum):
    SUCCESS = 0
    NO_WORLD = -1
    INVALID_SETTINGS = -2

def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'WorldTranslationExtractor',
        description = _('A tool to extracts translatable text from Minecraft worlds to facilitate localization.'),
    )

    parser.add_argument('--world', '-w', type=str, required=True, help=_('Path to the target world.'))
    parser.add_argument('--extract', '-e', type=str, action="append", help=_('An extractor to run over the world, multiple may be selected. If no extractors are specified, all available extractors will be run.'))

    return parser

def run() -> None:
    parser = get_argument_parser()
    args = parser.parse_args()
    run_terminal(args)

def run_terminal(args: argparse.Namespace) -> None:
    print(_('Incredible. It is spinning.'))

    try:
        w = world.try_load_world(args.world)
    except world.WorldLoadException as e:
        print(_('Could not load requested world: {}.\nExiting...').format(e))
        exit(ExitCode.NO_WORLD)

    try:
        s = settings.Settings.from_args(args)
    except settings.InvalidSettingsException as e:
        print(_('Invalid settings: {}\nExiting...').format(e))
        exit(ExitCode.INVALID_SETTINGS)

    print(s.extractors)
    extract.extract(w, s)
