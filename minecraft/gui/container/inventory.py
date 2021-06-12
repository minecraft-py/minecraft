from minecraft.gui.frame import Frame
from minecraft.gui.widget.image import Image
from minecraft.gui.widget.label import ColorLabel
from minecraft.source import resource_pack
from minecraft.utils.utils import *

import pyglet

class Inventory():

    def __init__(self, game):
        width, height = get_size()
        self.game = game
        self.frame = Frame(self.game, True)
        self._inventory = Image((width - 353) / 2, (height - 332) / 2,
                resource_pack.get_resource('textures/gui/containers/inventory').get_region(0, 90, 176, 166))
        self._inventory.sprite.scale = 2
        self._label = ColorLabel(text='Inventory', color='black', anchor_x='left', font_size=10,
            x=(width - 353) / 2 + 194, y=height - (height- 332) / 2 - 24)

        def on_resize(width, height):
            self._inventory.sprite.position = (width - 352) / 2, height - (height - 332) / 2
            self._label.x = (width - 353) / 2 + 194
            self._label.y = height - (height - 332) / 2 - 24

        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._inventory)
        self.frame.add_widget(self._label)
