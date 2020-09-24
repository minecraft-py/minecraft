import pyglet
from pyglet.text import decode_attributed

import time

from Minecraft.utils.utils import *


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
        log_info('dialogue add: %s' % text)
        try:
            decode_attributed(text)
        except:
            text = '{color (255, 0, 0, 255)}decode error'
        else:
            pass
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
            if len(self.dialogue) > 8192:
                self.dialogue.clear()
            self.shown.clear()
