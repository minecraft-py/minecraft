from os.path import join

from minecraft.gui.frame import Frame
from minecraft.gui.widget.image import Image
from minecraft.source import resource_pack
from minecraft.utils.utils import *

import pyglet

class Bag():

    def __init__(self, game):
        width, height = get_size()
        self.game = game
        self.frame = Frame(self.game, True)
        # 0 90 176 166
        # 264 249(1.5x)
        self._bag = Image((width - 264) / 2, (height - 249) / 2,
                resource_pack.get_resource('textures/gui/containers/inventory').get_region(0, 90, 176, 166))
        self._bag.sprite.scale = 1.5

        def on_resize(width, height):
            self._bag.sprite.position = (width - 264) / 2, (height - 249) / 2

        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._bag)
