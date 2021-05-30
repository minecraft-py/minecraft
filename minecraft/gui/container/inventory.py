from minecraft.gui.frame import Frame
from minecraft.gui.widget.image import Image
from minecraft.source import resource_pack
from minecraft.utils.utils import *

import pyglet

class Inventory():

    def __init__(self, game):
        width, height = get_size()
        self.game = game
        self.frame = Frame(self.game, True)
        self._inventory = Image((width - 264) / 2, (height - 249) / 2,
                resource_pack.get_resource('textures/gui/containers/inventory').get_region(0, 90, 176, 166))
        self._inventory.sprite.scale = 1.5

        def on_resize(width, height):
            self._inventory.sprite.position = (width - 264) / 2, (height - 249) / 2

        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._inventory)
