from Minecraft.gui.widget.base import Widget
from Minecraft.utils.utils import *

import pyglet
from pyglet.event import EventDispatcher
from pyglet.gl import *
from pyglet.graphics import Batch
from pyglet.shapes import Rectangle
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout


class DialogueEntry(Widget):

    def __init__(self):
        win_width, win_height = get_size()
        self.batch = Batch()
        self._doc = pyglet.text.document.UnformattedDocument('')
        self._doc.set_style(0, len(self._doc.text), dict(color=(255, 255, 255, 255)))
        font = self._doc.get_font()
        self.text_height = font.ascent - font.descent
        self.pad = 2
        self._outline = Rectangle(5 - self.pad, 20 - self.pad,
                get_size()[0] + self.pad - 5, self.text_height + self.pad, color=(0, 0, 0))
        self._outline.opacity = 150
        self._layout = IncrementalTextLayout(self._doc, get_size()[0] + self.pad - 5, self.text_height,
                multiline=False, batch=self.batch)
        self._caret = Caret(self._layout, color=(255, 255, 255))
        self._caret.visible = False
        self._layout.x = 5
        self._layout.y = 20
        self._focus = False
        self._press = False
        self.last_char = ''
        super().__init__(5, 20, get_size()[0] + self.pad - 5, self.text_height)

    def draw(self):
        self._outline.draw()
        self.batch.draw()

    def text(self, text):
        self._doc.text = text

    def _set_focus(self, value):
        self._focus = value
        self._caret.visible = value

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._focus:
            self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, y):
            get_game().set_cursor('text')
        else:
            get_game().set_cursor()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._press = True
            self._set_focus(True)
            self._caret.on_mouse_press(x, y, buttons, modifiers)
        else:
            self._set_focus(False)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._press:
            self._press = False

    def on_resize(self, width, height):
        self.width = width - self.pad - 5
        self._outline.width = width - self.pad - 5
        self._layout.width = width - self.pad - 5

    def on_text(self, text):
        if text == self.last_char:
            self.last_char = ''
            return
        else:
            self.last_char = text
        if self._focus:
            if text in ('\r', '\n'):
                self.dispatch_event('on_commit', self._layout.document.text)
                self._set_focus(False)
                return
            self._caret.on_text(text)

    def on_text_motion(self, motion):
        if self._focus:
            self._caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._focus:
            self._caret.on_text_motion_select(motion)

    def on_commit(self, text):
        pass


DialogueEntry.register_event_type('on_commit')


class TextEntry(Widget):

    def __init__(self, text, color, x, y, width, pad=3):
        win_width, win_height = get_size()
        self.batch = Batch()
        self._doc = pyglet.text.document.UnformattedDocument(text)
        self._doc.set_style(0, len(self._doc.text), dict(color=(255, 255, 255, 255)))
        font = self._doc.get_font()
        self.text_height = font.ascent - font.descent
        self.pad = pad
        self._outline = Rectangle(x - self.pad, win_height - y - self.pad,
                width + self.pad, self.text_height + self.pad, color=color[:3])
        self._outline.opacity = color[-1]
        self._layout = IncrementalTextLayout(width, self.text_height,
                multiline=False, batch=self.batch)
        self._caret = Caret(self._layout, color=(255, 255, 255))
        self._caret.visible = False
        self._layout.x = x
        self._layout.y = win_height - y
        self._focus = False
        self._press = False
        self.last_char = ''
        super().__init__(x, win_height - y, width, height)

    def draw(self):
        self._outline.draw()
        self.batch.draw()

    def text(self, text):
        self._doc.text = text

    def _set_focus(self, value):
        self._focus = value
        self._caret.visible = value

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._focus:
            self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x, y):
            get_game().set_cursor('text')
        else:
            get_game().set_cursor()

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._press = True
            self._set_focus(True)
            self._caret.on_mouse_press(x, y, buttons, modifiers)
        else:
            self._set_focus(False)

    def on_mouse_release(self, x, y, buttons, modifiers):
        if self._press:
            self._press = False

    def on_text(self, text):
        if text == self.last_char:
            self.last_char = ''
            return
        else:
            self.last_char = text
        if self._focus:
            if text in ('\r', '\n'):
                self.dispatch_event('on_commit', self._layout.document.text)
                self._set_focus(False)
                return
            self._caret.on_text(text)

    def on_text_motion(self, motion):
        if self._focus:
            self._caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self._focus:
            self._caret.on_text_motion_select(motion)

    def on_commit(self, text):
        pass


TextEntry.register_event_type('on_commit')
