# Copyright 2020-2022 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from esper import World


class EntityManager():
    """管理各实体。"""

    def __call__(self):
        self.entities = World()
