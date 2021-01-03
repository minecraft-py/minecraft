from Minecraft.gui.widget.base import Widget
from Minecraft.utils.utils import *

import pyglet
from pyglet.event import EventDispatcher
from pyglet.gl import *
from pyglet.graphics import Batch, vertex_list
from pyglet.text.caret import Caret
from pyglet.text.layout import IncrementalTextLayout


class TextEntry(Widget):

    def __init__(self, text, color, x, y, width):
        win_width, win_height = get_size()
        self.batch = Batch()
        self._doc = pyglet.text.document.UnformattedDocument(text)
        self._doc.set_style(0, len(self._doc.text), dict(color=(255, 255, 255, 255)))
        font = self._doc.get_font()
        height = font.ascent - font.descent
        pad = 2
        x1 = x - pad
        y1 = y - pad
        x2 = x + width + pad
        y2 = y + height + pad
        self._outline = vertex_list(4,
                                  ('v2i', [x1, y1, x2, y1, x2, y2, x1, y2]),
                                  ('c4B', color * 4))
        self._layout = IncrementalTextLayout(self._doc, width, height, multiline=False, batch=self.batch)
        self._caret = Caret(self._layout, color=(255, 255, 255))
        self._caret.visible = False
        self._layout.x = x
        self._layout.y = y
        self._focus = False
        super().__init__(x, y, width, height)
        self.last_char = ''

    def draw(self):
        self._outline.draw(GL_QUADS)
        self.batch.draw()

    def text(self, text):
        self._doc.text = text

    def _set_focus(self, value):
        self._focus = value
        self._caret.visible = value

    def on_mouse_motion(self, x, y, dx, dy):
        if self.check_hit(x,y):
            get_game().set_cursor('text')
        else:
            get_game().set_cursor(None)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if self._focus:
            self._caret.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

    def on_mouse_press(self, x, y, buttons, modifiers):
        if self.check_hit(x, y):
            self._set_focus(True)
            self._caret.on_mouse_press(x, y, buttons, modifiers)

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
