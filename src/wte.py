import settings
import extract
import world

import argparse
import shutil
import enum

class ExitCode(enum.IntEnum):
    SUCCESS = 0
    NO_WORLD = -1
    INVALID_SETTINGS = -2
    COULD_NOT_COPY = -3

def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'WorldTranslationExtractor',
        description = _('A tool to extract translatable text from Minecraft worlds to facilitate localization.'),
    )

    parser.add_argument('--world', '-w', type=str, required=True, help=_('Path to the target world.'))
    parser.add_argument('--out', '-o', type=str, help=_('Path to output a translated copy of the world. By default, outputs to <WORLD>_wte.'))
    parser.add_argument('--force', '-f', type=bool, action=argparse.BooleanOptionalAction, default=False, help=_('Delete previous contents of <OUT> before extracting.'))
    parser.add_argument('--lang', '-l', type=str, default='wte_lang.json', help=_('Path to output translation json. By default, outputs to wte_lang.json.'))
    parser.add_argument('--extract', '-e', type=str, action="append", help=_('An extractor to run over the world, multiple may be selected. If no extractors are specified, all available extractors will be run.'))

    return parser

def run() -> None:
    parser = get_argument_parser()
    args = parser.parse_args()
    run_terminal(args)
    exit(ExitCode.SUCCESS)

def run_terminal(args: argparse.Namespace) -> None:
    print(_('Incredible. It is spinning.'))

    path = f'{args.world}_wte' if args.out is None else args.out

    try:
        if args.force:
            shutil.rmtree(path)
        shutil.copytree(args.world, path, symlinks=False, ignore=None, copy_function=shutil.copy2, ignore_dangling_symlinks=False, dirs_exist_ok=False)
    except Exception as e:
        print(_('Could not copy world: {}.\nExiting...').format(e))
        exit(ExitCode.COULD_NOT_COPY)

    try:
        w = world.try_load_world(path)
    except world.WorldLoadException as e:
        print(_('Could not load requested world: {}.\nExiting...').format(e))
        exit(ExitCode.NO_WORLD)

    try:
        s = settings.Settings.from_args(args)
    except settings.InvalidSettingsException as e:
        print(_('Invalid settings: {}\nExiting...').format(e))
        exit(ExitCode.INVALID_SETTINGS)

    extract.extract(w, s)
