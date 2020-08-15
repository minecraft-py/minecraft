from .main import *

if __name__ == '__main__':
    window = Window(width=800, height=600, caption='Minecraft', resizable=True)
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()

