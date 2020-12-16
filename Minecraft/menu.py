from Minecraft.gui.frame import DialogueFrame
from Minecraft.gui.widget.button import Button
from Minecraft.utils.utils import *

import pyglet


class PauseMenu():

    def __init__(self, window):
        self.window = window
        self.frame = DialogueFrame(self.window)
        self._back_button = Button((self.window.width - 200) / 2, 100, 200, 40, 'Back to game')
        self._exit_button = Button((self.window.width - 200) / 2, 150, 200, 40, 'Exit')

        def on_back_press():
            self.window.set_exclusive_mouse(True)
            self.frame.enable(False)

        def on_exit_press():
            self.window.save(0)
            self.window.on_close()
            exit(0)

        setattr(self._back_button, 'on_press', on_back_press)
        setattr(self._exit_button, 'on_press', on_exit_press)
        self.frame.add_widget(self._back_button)
        self.frame.add_widget(self._exit_button)
