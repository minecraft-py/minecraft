# minecraftpy, a sandbox game
# Copyright (C) 2020-2023 minecraftpy team
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
from atexit import register
from locale import getdefaultlocale
from logging import config, getLogger
from pathlib import Path
from textwrap import dedent
from uuid import UUID

from minecraft.resource.loader import GameAssets
from minecraft.utils import *
from minecraft.utils.logging import config as logging_config
from minecraft.utils.prepare import create_storage_path, print_debug_info
from minecraft.utils.setting import Setting

try:
    import esper
    major, minor = [int(s) for s in esper.version.split(".")]
    assert (major == 2) and (minor == 5)

    import opensimplex
    major, minor, patch = [int(s) for s in opensimplex.__version__.split(".")]
    assert (major == 0) and (minor == 4) and (patch == 5)

    import PIL
    major, minor, patch = [int(s) for s in PIL.__version__.split(".")]
    assert (major == 10) and (minor == 0) and (patch == 0)

    import pyglet
    major, minor, patch = [int(s) for s in pyglet.version.split(".")]
    assert (major == 2) and (minor == 0) and (patch == 8)
except (AssertionError, ModuleNotFoundError):
    print(dedent("""\
    One or more dependencies are not installed or the wrong version
    is installed. Please check if the following packages are correctly
    installed on your computer:

    \tesper       2.5
    \topensimplex 0.4.5
    \tpillow      10.0.0
    \tpyglet      2.0.8
    """))
    input("Press ENTER after you read the above information...")
    exit(1)

parser = argparse.ArgumentParser(
    description="A sandbox game", prog="minecraft")
parser.add_argument("-D", "--dir", help="storage location", metavar="DIR")
parser.add_argument("-I", "--include",
                    help="add paths to `sys.path`", metavar="PATH")
parser.add_argument("-L", "--extlib", help="add extra lib", metavar="LIB")
parser.add_argument("--player", help="player information", metavar="name:uuid")
parser.add_argument("-V", "--version", action="version",
                    version="%(prog)s " + VERSION["str"] + ("(stable)" if VERSION["stable"] else "(in develop)"))
cmdargs = parser.parse_args()

if cmdargs.dir is not None:
    STORAGE_DIR = Path(cmdargs.dir)
create_storage_path(get_storage_path())
config.dictConfig(logging_config)
print_debug_info()

logger = getLogger(__name__)
assets = GameAssets()

player_info: dict
if cmdargs.player is not None:
    player_name, player_uuid = cmdargs.player.split(":", 1)
    player_uuid = UUID(player_uuid)
    player_info = {
        "name": player_name,
        "uuid": player_uuid
    }
else:
    logger.error(
        "A player information should be provided through `--player` argument")
    exit(1)

setting = Setting()
if setting.get("language", "<auto>") == "<auto>":
    lang_code = getdefaultlocale()[0].lower()
else:
    lang_code = setting.get("language", "en_us").lower()

__all__ = ("cmdargs", "assets", "player_info", "setting")


@register
def _():
    logger.info("This log file is stored in: %s",
                logging_config["handlers"]["file"]["filename"])
