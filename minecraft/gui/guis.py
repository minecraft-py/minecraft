from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button, ChoseButton
from minecraft.gui.widget.entry import DialogueEntry
from minecraft.source import resource_pack, player
from minecraft.utils.utils import *

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
                    # 将对话中的 ${pos}, ${chk} 替换为玩家的位置及所在区块
                    text = text.replace('${pos}', ' '.join([str(int(pos)) for pos in self.game.player['position']]))
                    text = text.replace('${chk}', ' '.join([str(int(pos)) for pos in self.game.sector]))
                    self.game.dialogue.add_dialogue('<%s> %s' % (player['name'], text))
            self._entry.text('')
            self.game.toggle_gui()
        
        self._entry.register_event('commit', on_commit)

    def text(self, text=''):
        self._entry.text(text)


class PauseMenu():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game, True)
        self._back_button = Button((self.game.width - 200) / 2, 100, 200, 40, resource_pack.get_translation('game.pause_menu.back_to_game'))
        self._exit_button = Button((self.game.width - 200) / 2, 150, 200, 40, resource_pack.get_translation('game.pause_menu.exit'))

        def on_back_press():
            self.game.toggle_gui()

        def on_exit_press():
            self.game.save(0)
            self.game.on_close()
            exit(0)

        def on_resize(width, height):
            h = get_size()[1]
            self._back_button.x = (self.game.width - 200) / 2
            self._back_button.y = 100
            self._exit_button.x = (self.game.width - 200) / 2
            self._exit_button.y = 150

        self._back_button.register_event('press', on_back_press)
        self._exit_button.register_event('press', on_exit_press)
        self.frame.register_event('resize', on_resize)
        self.frame.add_widget(self._back_button)
        self.frame.add_widget(self._exit_button)
