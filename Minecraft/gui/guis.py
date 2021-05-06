from Minecraft.gui.frame import Frame
from Minecraft.gui.widget.button import Button, ChoseButton
from Minecraft.gui.widget.entry import DialogueEntry
from Minecraft.source import lang, player
from Minecraft.utils.utils import *

import pyglet


class Chat():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game, True)
        self._entry = DialogueEntry()
        self.frame.add_widget(self._entry)

        def on_commit(text):
            if text != '':
                self.game.dialogue.history.append(text)
                if text.startswith('/'):
                    self.game.run_command(text[1:])
                else:
                    text = text.replace('(position)', ' '.join([str(int(pos)) for pos in self.game.player['position']]))
                    text = text.replace('(chunk)', ' '.join([str(int(pos)) for pos in self.game.sector]))
                    self.game.dialogue.add_dialogue('<%s> %s' % (player['name'], text))
            self.game.player['in_gui'] = False
            self.game.player['in_chat'] = False
            self._entry.text('')
            self.game.guis['chat'].frame.enable(False)
            self.game.set_exclusive_mouse(True)
        
        self._entry.register_event('commit', on_commit)

    def text(self, text=''):
        self._entry.text(text)


class PauseMenu():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game, True)
        self._back_button = Button((self.game.width - 200) / 2, 100, 200, 40, lang['game.pause_menu.back_to_game'])
        self._exit_button = Button((self.game.width - 200) / 2, 150, 200, 40, lang['game.pause_menu.exit'])

        def on_back_press():
            self.game.set_exclusive_mouse(True)
            self.game.player['in_gui'] = False
            self.game.player['pause'] = False
            self.frame.enable(False)

        def on_exit_press():
            self.game.save(0)
            self.game.on_close()
            exit(0)

        def on_resize(width, height):
            self._back_button.x = (self.game.width - 200) / 2
            self._back_button.y = 100
            self._exit_button.x = (self.game.width - 200) / 2
            self._exit_button.y = 150

        self._back_button.register_event('press', on_back_press)
        self._exit_button.register_event('press', on_exit_press)
        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._back_button)
        self.frame.add_widget(self._exit_button)
