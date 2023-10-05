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

from __future__ import annotations
from json import loads
from typing import Dict, List, Union

from minecraft import assets
from minecraft.utils.namespace import NameSpace, get_namespace

_model_cache: Dict[tuple, BlockModel] = {}


class BlockModel:
    """Block Model."""

    def __init__(self):
        self.block_json: dict = {}
        self.gui_light: str = ""
        self.display: Dict[str, Dict[str, List[float]]] = {}
        self.parent: BlockModel = None
        self.element: List[BlockModelElement] = []
        self.textures: BlockModelTextures = None

    @classmethod
    def from_namespace(self, namespace: Union[str, NameSpace]) -> BlockModel:
        if not isinstance(namespace, NameSpace):
            namespace = get_namespace(namespace)
        block_name = namespace.sub[-1]
        if (namespace.main, block_name) not in _model_cache:
            cls = BlockModel()
            cls.block_json = loads(
                assets.loader.file("models/block/%s.json" % block_name, mode="rb")
                .read()
                .decode("utf-8")
            )
            if "parent" in cls.block_json:
                parent_block = get_namespace(cls.block_json["parent"]).sub[-1]
                cls.parent = BlockModel.from_namespace(parent_block)
            cls.gui_light = cls.get("gui_light", "side")
            cls.display = cls.get("display", {})
            _model_cache[(namespace.main, block_name)] = cls
        else:
            cls = _model_cache[(namespace.main, block_name)]
        return cls

    def get(self, key: str, default=None):
        if key in self.block_json:
            return self.block_json[key]
        elif self.parent is not None:
            return self.parent.get(key, default)
        else:
            return default


class BlockModelElement:
    def __init__(self):
        self.face: Dict[str, BlockModelElementFace] = {}


class BlockModelElementFace:
    pass


class BlockModelTextures:
    pass


__all__ = (
    "BlockModel",
    "BlockModelElement",
    "BlockModelElementFace",
    "BlockModelTextures",
)
