# Minecraft 启动器

import os
from tkinter import Listbox, Tk
import tkinter.ttk as ttk

from Minecraft.game import *
import pyglet


class MinecraftLauncher(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title('Minecraft Launcher')
        # 小部件
        self.new_button = ttk.Button(self, text='New')
        self.new_button.state(['disabled'])
        self.start_button = ttk.Button(self, text='Start', command=self.start_game)
        self.exit_button = ttk.Button(self, text='Exit',  command=lambda: exit())
        self.game_item_list = Listbox(self, height=12)
        self.vscroll = ttk.Scrollbar(self, orient='vertical', command=self.game_item_list.yview)
        self.game_item_list.configure(yscrollcommand=self.vscroll.set)
        for item in os.listdir('resource/save'):
            self.game_item_list.insert('end', item)
        self.del_button = ttk.Button(self, text='Delete')
        self.del_button.state(['disabled'])
        self.rename_button = ttk.Button(self, text='Rename')
        self.rename_button.state(['disabled'])
        # 显示
        self.new_button.grid(column=0, row=0, padx=5, pady=5)
        self.start_button.grid(column=1, row=0, padx=5, pady=5)
        self.exit_button.grid(column=2, row=0, padx=5, pady=5)
        self.game_item_list.grid(column=0, columnspan=4, row=1, padx=3, pady=5, sticky='news' )
        self.vscroll.grid(column=4, row=1, padx=2, pady=5, sticky='nes')
        self.del_button.grid(column=1, row=2, padx=5, pady=5)
        self.rename_button.grid(column=2, row=2, padx=5, pady=5)
        self.resizable(False, False)

    def start_game(self, event=None):
        self.iconify()
        window = Window(width=800, height=600, caption='Minecraft', resizable=True)
        window.set_exclusive_mouse(True)
        setup()
        pyglet.app.run()
        self.deiconify()

