from Minecraft.gui.frame import DialogueFrame
from Minecraft.gui.widget.button import Button
from Minecraft.utils.utils import *

import pyglet


class PauseMenu():

    def __init__(self, window):
        self.window = window
        self.frame = DialogueFrame(self.window)
        self._exit_button = Button(100, 100, 100, 40, 'Exit')
        setattr(self._exit_button, 'on_press', lambda: log_info('click'))
        self.frame.add_widget(self._exit_button)
