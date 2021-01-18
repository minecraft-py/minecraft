from Minecraft.gui.frame import DialogueFrame
from Minecraft.gui.widget.button import Button, ChoseButton
from Minecraft.gui.widget.text import TextEntry
from Minecraft.source import lang, player
from Minecraft.utils.utils import *

import pyglet


class Chat():

    def __init__(self, window):
        self.window = window
        self.frame = DialogueFrame(self.window)
        self._entry = TextEntry('', (0, 0, 0, 150), 5, 20, 400)
        self.frame.add_widget(self._entry)

        def on_commit(text):
            if text != '':
                if text.startswith('/'):
                    self.window.run_command(text[1:])
                else:
                    self.window.dialogue.add_dialogue('<%s> %s' % (player['name'], text))
            self.window.player['in_chat'] = False
            self._entry.text('')
            self.window.menu['chat'].frame.enable(False)
            self.window.set_exclusive_mouse(True)

        setattr(self._entry, 'on_commit', on_commit)

    def text(self, text=''):
        self._entry.text(text)


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
