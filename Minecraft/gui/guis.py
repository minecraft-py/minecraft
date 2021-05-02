from Minecraft.gui.frame import Frame
from Minecraft.gui.widget.button import Button, ChoseButton
from Minecraft.gui.widget.entry import DialogueEntry
from Minecraft.source import lang, player
from Minecraft.utils.utils import *

import pyglet


class Chat():

    def __init__(self, window):
        self.window = window
        self.frame = Frame(self.window, True)
        self._entry = DialogueEntry()
        self.frame.add_widget(self._entry)

        def on_commit(text):
            if text != '':
                self.window.dialogue.history.append(text)
                if text.startswith('/'):
                    self.window.run_command(text[1:])
                else:
                    self.window.dialogue.add_dialogue('<%s> %s' % (player['name'], text))
            self.window.player['in_chat'] = False
            self._entry.text('')
            self.window.guis['chat'].frame.enable(False)
            self.window.set_exclusive_mouse(True)
        
        self._entry.register_event('commit', on_commit)

    def text(self, text=''):
        self._entry.text(text)


class PauseMenu():

    def __init__(self, window):
        self.window = window
        self.frame = Frame(self.window, True)
        self._back_button = Button((self.window.width - 200) / 2, 100, 200, 40, lang['game.pause_menu.back_to_game'])
        self._exit_button = Button((self.window.width - 200) / 2, 150, 200, 40, lang['game.pause_menu.exit'])

        def on_back_press():
            self.window.set_exclusive_mouse(True)
            self.frame.enable(False)

        def on_exit_press():
            self.window.save(0)
            self.window.on_close()
            exit(0)

        def on_resize(width, height):
            self._back_button.x = (self.window.width - 200) / 2
            self._back_button.y = 100
            self._exit_button.x = (self.window.width - 200) / 2
            self._exit_button.y = 150

        self._back_button.register_event('press', on_back_press)
        self._exit_button.register_event('press', on_exit_press)
        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._back_button)
        self.frame.add_widget(self._exit_button)
