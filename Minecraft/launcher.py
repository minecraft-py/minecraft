# Minecraft 启动器

import os
import re
from tkinter import Listbox, Tk, Toplevel, messagebox
import tkinter.ttk as ttk

from Minecraft.game import *
from Minecraft.source import path, lang
import pyglet

def is_game_restore(name):
    """
    判断一个目录是否为游戏存档

    @param name 要检查的游戏目录
    """
    if os.path.isdir(os.path.join(path['save'], name)):
        if ('%s.world' % name) in os.listdir(os.path.join(path['save'], name)):
            if ('%s.player' % name) in os.listdir(os.path.join(path['save'], name)):
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class MinecraftLauncher(Tk):

    def __init__(self):
        try:
            Tk.__init__(self)
        except:
            print('[err] No display, exit')
            exit(1)
        self.title(lang['launcher.title'])
        # 小部件
        self.new_button = ttk.Button(self, text=lang['launcher.new'], command=self.new)
        self.start_button = ttk.Button(self, text=lang['launcher.start'], command=self.start_game)
        self.exit_button = ttk.Button(self, text=lang['launcher.exit'],  command=lambda: exit())
        self.game_item_list = Listbox(self, height=12)
        self.vscroll = ttk.Scrollbar(self, orient='vertical', command=self.game_item_list.yview)
        self.game_item_list.configure(yscrollcommand=self.vscroll.set)
        self.del_button = ttk.Button(self, text=lang['launcher.delete'], command=self.delete)
        self.rename_button = ttk.Button(self, text=lang['launcher.rename'], command=self.rename)
        # 显示
        self.new_button.grid(column=0, row=0, padx=5, pady=5)
        self.start_button.grid(column=1, row=0, padx=5, pady=5)
        self.exit_button.grid(column=2, row=0, padx=5, pady=5)
        self.game_item_list.grid(column=0, columnspan=4, row=1, padx=3, pady=5, sticky='news')
        self.vscroll.grid(column=4, row=1, padx=2, pady=5, sticky='nes')
        self.del_button.grid(column=1, row=2, padx=5, pady=5)
        self.rename_button.grid(column=2, row=2, padx=5, pady=5)
        self.resizable(False, False)
        self.refresh()

    def delete(self, event=None):
        if self.game_item_list.curselection() == ():
            select = self.game_item_list.get(0)
        else:
            select = self.game_item_list.get(self.game_item_list.curselection()[0])
        if messagebox.askyesno(message=lang['launcher.dialog.text.delete'] % select,
                title=lang['launcher.dialog.title.delete']):
            os.remove(os.path.join(path['save'], select, '%s.world' % select))
            os.remove(os.path.join(path['save'], select, '%s.player' % select))
            os.rmdir(os.path.join(path['save'], select))
        else:
            pass
        self.refresh()

    def new(self, event=None):
        self.new_dialog = Toplevel(self)
        self.new_dialog.title(lang['launcher.dialog.title.new'])
        self.new_dialog_label_name = ttk.Label(self.new_dialog, text=lang['launcher.dialog.text.name'])
        self.new_dialog_entry_name = ttk.Entry(self.new_dialog)
        self.new_dialog_button_ok = ttk.Button(self.new_dialog, text=lang['launcher.dialog.text.ok'], command=self.new_world)
        self.new_dialog_label_name.grid(column=0, row=0, padx=5, pady=5)
        self.new_dialog_entry_name.grid(column=1, row=0, columnspan=2, padx=5, pady=5)
        self.new_dialog_button_ok.grid(column=2, row=1, padx=5, pady=5)
        self.new_dialog.resizable(False, False)
        self.new_dialog.geometry('+%d+%d' % (self.winfo_x() + 50, self.winfo_y() + 50))
        self.new_dialog.transient(self)
        self.new_dialog.deiconify()
        self.new_dialog.grab_set()
        self.new_dialog.wait_window()
        self.new_dialog.mainloop()

    def new_world(self, event=None):
        name = self.new_dialog_entry_name.get()
        if name == '':
            return
        elif not re.match(r'^([a-z]|[A-Z]|_)\w+$', name):
            return
        else:
            if not os.path.isdir(os.path.join(path['save'], name)):
                os.mkdir(os.path.join(path['save'], name))
                world = open(os.path.join(path['save'], name, '%s.world' % name), 'w+')
                world.write('{}\n')
                world.close()
                player = {'position': '0.0 3.8 0.0', 'respawn': '0.0 3.8 0.0', 'bag': 'grass'}
                json.dump(player, open(os.path.join(path['save'], name, '%s.player' % name), 'w+'), indent='\t')
                self.new_dialog.destroy()
        self.refresh()

    def refresh(self):
        self.game_item_list.delete(0, 'end')
        for item in [i for i in os.listdir(path['save']) if is_game_restore(i)]:
            self.game_item_list.insert('end', item)

    def rename(self):
        self.rename_dialog = Toplevel(self)
        self.rename_dialog.title(lang['launcher.dialog.title.rename'])
        self.rename_dialog_label = ttk.Label(self.rename_dialog, text=lang['launcher.dialog.text.name'])
        self.rename_dialog_entry = ttk.Entry(self.rename_dialog)
        if self.game_item_list.curselection() == ():
            self.rename_dialog_entry.insert(0, self.game_item_list.get(0))
        else:
            self.rename_dialog_entry.insert(0, self.game_item_list.curselection()[0])
        self.old = os.path.join(path['save'], self.rename_dialog_entry.get())
        self.rename_dialog_button = ttk.Button(self.rename_dialog, text=lang['launcher.dialog.text.ok'],
                command=self.rename_world)
        self.rename_dialog_label.grid(column=0, row=0, padx=5, pady=5)
        self.rename_dialog_entry.grid(column=1, row=0, columnspan=2, padx=5, pady=5)
        self.rename_dialog_button.grid(column=2, row=1, padx=5, pady=5)
        self.rename_dialog.resizable(False, False)
        self.rename_dialog.geometry('+%d+%d' % (self.winfo_x() + 50, self.winfo_y() + 50))
        self.rename_dialog.transient(self)
        self.rename_dialog.deiconify()
        self.rename_dialog.grab_set()
        self.rename_dialog.wait_window()
        self.rename_dialog.mainloop()

    def rename_world(self):
        self.rename_dialog.destroy()
        self.refresh()

    def start_game(self, event=None):
        if self.game_item_list.curselection() == ():
            select = self.game_item_list.get(0)
        else:
            select = self.game_item_list.get(self.game_item_list.curselection()[0])
        self.iconify()
        window = Window(width=800, height=600, caption='Minecraft', resizable=True)
        window.set_name(select)
        window.set_exclusive_mouse(False)
        setup()
        pyglet.app.run()
        self.destroy()

