from Minecraft.main import *

if __name__ == '__main__':
    window = Window(width=800, height=600, caption='Minecraft', resizable=True)
    # 隐藏鼠标并防止其离开窗口
    window.set_exclusive_mouse(True)
    setup()
    pyglet.app.run()

