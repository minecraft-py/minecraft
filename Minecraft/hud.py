# 游戏用户界面小部件

import pyglet
from pyglet.text import decode_attributed
from pyglet.shapes import Rectangle
import time


class Bag():
    # 按 E 键打开的背包

    def __init__(self, x, y, width, height):
        self._element = {}
        self._element['seq'] = Rectangle(x, y, width, height, color=(200, 200, 200))

    def draw(self):
        self._element['seq'].draw()

    def resize(self, x, y, width, height):
        self._element['seq'].position = (x, y)
        self._element['seq'].width = width
        self._element['seq'].height = height


class Dialogue():
    # 显示在左面的聊天记录

    def __init__(self, width, height):
        self.dialogue_label = pyglet.text.DocumentLabel(decode_attributed(''),
                x=0, y=height - 75, width=width // 2, multiline=True)
        # 全部聊天内容
        self.dialogue = []
        # 实际显示的聊天内容
        self.shown = []
        # 最后一条聊天发送的时间
        self.last = time.time()

    def add_dialogue(self, text):
        print('[info][%s] dialogue add: %s' % (time.strftime('%H:%M:%S'), text))
        self.dialogue.append(text)
        self.last = time.time()
        if len(self.shown) < 10:
            self.shown.append(text)
        else:
            self.shown.pop(0)
            self.shown.append(text)

    def draw(self):
        # 两个换行符表示真正的换行
        text = decode_attributed('{color (255, 255, 255, 255)}{background_color (0, 0, 0, 64)}' + '\n\n'.join(self.shown))
        self.dialogue_label.document = text
        self.dialogue_label.draw()
        
    def resize(self, width, height):
        self.dialogue_label.x = 0
        self.dialogue_label.y = height - 75
        self.dialogue_label.width = width // 2

    def update(self):
        if time.time() - self.last > 10.0:
            self.shown.clear()
