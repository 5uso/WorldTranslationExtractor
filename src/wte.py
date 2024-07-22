import settings
import extract
import world

import argparse
import shutil
import enum

from amulet.api.errors import ChunkLoadError

class ExitCode(enum.IntEnum):
    INTERRUPTED = 1
    SUCCESS = 0
    NO_WORLD = -1
    INVALID_SETTINGS = -2
    COULD_NOT_COPY = -3
    CHUNK_LOAD_ERROR = -4
    KEY_ERROR = -5

def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'WorldTranslationExtractor',
        description = _('A tool to extract translatable text from Minecraft worlds to facilitate localization.'),
    )

    parser.add_argument('--world', '-w', type=str, required=True, help=_('Path to the target world.'))
    parser.add_argument('--out', '-o', type=str, help=_('Path to output a translated copy of the world. By default, outputs to <WORLD>_wte.'))
    parser.add_argument('--force', '-f', type=bool, action=argparse.BooleanOptionalAction, default=False, help=_('Delete previous contents of <OUT> before extracting.'))
    parser.add_argument('--lang', '-l', type=str, default='wte_lang.json', help=_('Path to output translation json. By default, outputs to wte_lang.json.'))
    parser.add_argument('--extract', '-e', type=str, action='append', help=_('An extractor to run over the world, multiple may be selected. If no extractors are specified, all available extractors will be run.'))
    parser.add_argument('--dimension', '-d', type=str, action='append', help=_('A dimension to scan, multiple may be selected. If no dimensions are specified, all dimensions will be scanned.'))
    parser.add_argument('--keepdup', '-k', type=bool, action=argparse.BooleanOptionalAction, default=False, help=_('Keep duplicate translation texts as separate keys.'))
    parser.add_argument('--sort', '-s', type=bool, action=argparse.BooleanOptionalAction, default=False, help=_('Sort output json alphabetically.'))
    parser.add_argument('--indent', '-i', type=int, default=2, help=_('Amount of spaces used to indent the output json.'))
    parser.add_argument('--batch', '-b', type=int, default=5000, help=_('When iterating the world, save every <BATCH> chunks.'))
    parser.add_argument('--versionless', '-v', type=bool, action=argparse.BooleanOptionalAction, default=False, help=_('Ignore extractor data version incompatibilities.'))

    return parser

def run() -> None:
    parser = get_argument_parser()
    args = parser.parse_args()
    run_terminal(args)
    exit(ExitCode.SUCCESS)

def run_terminal(args: argparse.Namespace) -> None:
    print(_('Creating working copy of the world...'))

    path = f'{args.world}_wte' if args.out is None else args.out

    try:
        if args.force:
            try:
                shutil.rmtree(path)
            except FileNotFoundError as e:
                pass
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
        s = settings.Settings.from_args(args, w.data_version)
    except settings.InvalidSettingsException as e:
        print(_('Invalid settings: {}\nExiting...').format(e))
        exit(ExitCode.INVALID_SETTINGS)

    try:
        extract.extract(w, s)
    except KeyboardInterrupt:
        print(_('Extraction interrupted. Output file partially translated.\nExiting...'))
        exit(ExitCode.INTERRUPTED)
    except ChunkLoadError as e:
        print(_('Error loading chunk: {}\nThis error may indicate the version of amulet you\'re using is not compatible with your Minecraft version.\nExiting...').format(e))
        exit(ExitCode.CHUNK_LOAD_ERROR)
    except KeyError as e:
        print(_('Error accessing tag: {}\nThis error may indicate the current extractors are not compatible with your Minecraft version.\nExiting...').format(e))
        exit(ExitCode.KEY_ERROR)
