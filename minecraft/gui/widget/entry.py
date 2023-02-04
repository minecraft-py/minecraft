# Copyright 2020-2023 Minecraft-in-python.
# SPDX-License-Identifier: GPL-3.0-only

from minecraft.gui.widget import InputWidget
from minecraft.utils.utils import *
from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout
from pyglet.text.document import UnformattedDocument


class TextEntry(InputWidget):
    """文本框。"""

    def __init__(self, x, y, width, text=""):
        pass