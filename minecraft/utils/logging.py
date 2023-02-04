# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

import logging.config
from time import strftime
from os import path

from minecraft.utils.utils import storage_dir


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
            "filename": path.join(storage_dir(), "log", strftime("%Y-%m-%d_%H.%M.%S.log"))
        }
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "DEBUG"
    }
}
logging.config.dictConfig(config)
