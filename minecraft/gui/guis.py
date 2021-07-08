from minecraft.gui.frame import Frame
from minecraft.gui.widget.button import Button, ChooseButton
from minecraft.gui.widget.entry import DialogueEntry
from minecraft.gui.widget.label import ColorLabel
from minecraft.source import resource_pack, player
from minecraft.utils.utils import *

import pyglet


class Chat():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game)
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


class DieScreen():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game, True)
        self.frame.set_background_color((220, 0, 0, 100))
        self._text_die = ColorLabel(text=resource_pack.get_translation('game.text.die'),
                x=self.game.width / 2, y=0.8 * self.game.height, font_size=42, anchor_x='center', anchor_y='center')
        self._text_reason = ColorLabel(text=get_game().player['die_reason'], anchor_x='center', anchor_y='center',
                x=self.game.width / 2, y=0.7 * self.game.height, font_size=15)
        self._respawn = Button(((self.game.width - 200) / 2), 0.7 * self.game.height, 200, 40,
                resource_pack.get_translation('game.text.respawn'))

        def on_press():
            self.game.player['die'] = False
            self.game.player['position'] = self.game.player['respawn_position']
            self.game.toggle_gui()

        def on_resize(width, height):
            self._text_die.x = width / 2
            self._text_die.y = 0.8 * height
            self._text_reason.x = width / 2
            self._text_reason.y = 0.7 * height
            self._respawn.x = (width - 200) / 2
            self._respawn.y = 0.7 * height

        def on_die():
            self._text_reason.text = get_game().player['die_reason']

        self.frame.add_widget(self._text_die)
        self.frame.add_widget(self._text_reason)
        self.frame.add_widget(self._respawn)
        get_game().register_event('die', on_die)
        self.frame.register_event('resize', on_resize)
        self._respawn.register_event('press', on_press)


class PauseMenu():

    def __init__(self, game):
        self.game = game
        self.frame = Frame(self.game, True)
        self._back_button = Button((self.game.width - 200) / 2, 100, 200, 40,
                resource_pack.get_translation('game.gui.pause_menu.back_to_game'))
        self._exit_button = Button((self.game.width - 200) / 2, 150, 200, 40,
                resource_pack.get_translation('game.gui.pause_menu.exit'))

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

        self.frame.add_widget(self._back_button)
        self.frame.add_widget(self._exit_button)
        self.frame.register_event('resize', on_resize)
        self._back_button.register_event('press', on_back_press)
        self._exit_button.register_event('press', on_exit_press)
