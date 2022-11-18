# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from sys import argv
from time import strftime
from os import path

from minecraft.utils.utils import search_mcpy


log_file = strftime("%Y-%m-%d_%H.%M.%S.log")
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s %(levelname)-8s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "default",
            "level": "DEBUG",
            "filename": path.join(search_mcpy(), "log", log_file)
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}
