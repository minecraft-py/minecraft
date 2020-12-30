from Minecraft.gui.frame import DialogueFrame
from Minecraft.gui.widget.button import Button
from Minecraft.gui.widget.text import TextEntry
from Minecraft.source import lang
from Minecraft.utils.utils import *

import pyglet


class Chat():

    def __init__(self, window):
        self.window = window
        self.frame = DialogueFrame(self.window)
        self._entry = TextEntry('', (0.0, 0.0, 0.0, 0.4), 0, 20, 100)
        self.frame.add_widget(self._entry)


class PauseMenu():

    def __init__(self, window):
        self.window = window
        self.frame = DialogueFrame(self.window)
        self._back_button = Button((self.window.width - 200) / 2, 100, 200, 40, lang['game.pause_menu.back_to_game'])
        self._exit_button = Button((self.window.width - 200) / 2, 150, 200, 40, lang['game.pause_menu.exit'])

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
