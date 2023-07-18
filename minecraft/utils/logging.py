# minecraftpy, a sandbox game
# Copyright (C) 2020-2023 Minecraftpy team
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

from time import strftime
from os import path

from minecraft.utils import get_storage_path

config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(threadName)s/%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "DEBUG",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "level": "DEBUG",
            "filename": path.join(get_storage_path(), "log", strftime("%Y-%m-%d_%H.%M.%S.log"))
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}

__all__ = ("config")
