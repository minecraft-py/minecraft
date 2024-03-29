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

from json import dump
from logging import getLogger
from os import makedirs, mkdir
from pathlib import Path
from platform import platform, python_version_tuple
from shlex import join
from sys import argv

from pyglet.gl import gl_info

from minecraft.utils import VERSION

logger = getLogger(__name__)


def create_storage_path(p: Path):
    if p.exists():
        return
    makedirs(p, exist_ok=True)
    for subpath in ["log", "saves", "screenshot"]:
        mkdir(p / subpath)
    setting = {"fov": 70, "fps": 60, "language": "<auto>"}
    dump(setting, open(p / "setting.json", "w+"))


def print_debug_info():
    logger.debug("** Start Minecraftpy **")
    logger.debug("Operation system: %s", platform())
    logger.debug(
        "Python version: %s", ".".join([str(s) for s in python_version_tuple()[:3]])
    )
    logger.debug("OpenGL version: %s", gl_info.get_version_string())
    logger.debug("Renderer: %s" % gl_info.get_renderer())
    logger.debug(
        "Minecraftpy version: %s (data version: %d)", VERSION["str"], VERSION["data"]
    )
    logger.debug("Command line arguments: %s", join(argv[1:]))


__all__ = ("create_storage_path", "print_debug_info")
