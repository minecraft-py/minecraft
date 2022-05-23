from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button
from minecraft.gui.widget.label import ColorLabel
from minecraft.gui.widget.loading import LoadingBackground
from minecraft.scene import Scene
from minecraft.sources import resource_pack
from minecraft.utils.utils import *
from pyglet.window import key


class SinglePlayerScene(Scene):

    def __init__(self):
        super().__init__()
        width, height = get_size()
        self._back = LoadingBackground()
        self._title = ColorLabel(resource_pack.get_translation("text.single_player_scene.choose_a_save"),
                                 x=width // 2, y=0.95 * height, anchor_x="center", anchor_y="center", font_size=15)
    
    def on_draw(self):
        self._back.draw()
        self._title.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            get_game().switch_scene("start")
            return True

    def on_resize(self, width, height):
        self._back.resize(width, height)
        self._title.x = width // 2
        self._title.y = 0.95 * height 
