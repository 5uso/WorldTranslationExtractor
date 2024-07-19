import settings
import world

import argparse
import enum

class ExitCode(enum.IntEnum):
    SUCCESS = 0
    NO_WORLD = -1
    INVALID_SETTINGS = -2

def get_argument_parser():
    parser = argparse.ArgumentParser(
        prog = 'WorldTranslationExtractor',
        usage = _('./main.py -w <world_path> [options]'),
        description = _('A tool to extracts translatable text from Minecraft worlds to facilitate localization.'),
    )

    parser.add_argument('--world', '-w', type=str, required=True, help='Path to the target world')

    return parser

def run():
    parser = get_argument_parser()
    args = parser.parse_args()
    run_terminal(args)

def run_terminal(args: argparse.Namespace):
    print(_('Incredible. It is spinning.'))

    try:
        w = world.try_load_world(args.world)
    except world.WorldLoadException as e:
        print(_('Could not load requested world. Exiting...'))
        exit(ExitCode.NO_WORLD)

    try:
        s = settings.Settings.from_args(args)
    except settings.InvalidSettingsException as e:
        print(_('Invalid settings. Exiting...'))
        exit(ExitCode.INVALID_SETTINGS)

    print(args)
