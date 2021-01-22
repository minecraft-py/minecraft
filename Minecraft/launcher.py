import os
import json
import shutil
from string import punctuation
import time
import traceback
from tkinter import Listbox, Tk, Toplevel, messagebox
import tkinter.ttk as ttk

from Minecraft.utils.utils import *
log_info('loading game lib')
from Minecraft.game import *
from Minecraft.archiver import load_window
from Minecraft.repair import repair_archive
from Minecraft.source import get_lang, path, settings
from Minecraft.utils.utils import *
log_info('start launcher')

import pyglet

def is_game_restore(name):
    """
    判断一个目录是否为游戏存档

    :param: name 要检查的游戏目录
    """
    if name == '_server':
        return False
    if os.path.isdir(os.path.join(path['save'], name)):
        if 'world.json' in os.listdir(os.path.join(path['save'], name)):
            if 'info.json' in os.listdir(os.path.join(path['save'], name)):
                if 'player.json' in os.listdir(os.path.join(path['save'], name)):
                    return True
                else:
                    return False
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
            log_err('no display, exit')
            exit(1)
        self.title(get_lang('launcher.title'))
        if settings['use-theme'] != 'ttk':
            theme_path = os.path.dirname(os.path.abspath(__file__)) + '/theme/' + settings['use-theme']
            self.tk.eval('lappend auto_path {%s}' % theme_path)
            ttk.Style().theme_use(settings['use-theme'])
        # 小部件
        self.new_button = ttk.Button(self, text=get_lang('launcher.new'), command=self.new)
        self.start_button = ttk.Button(self, text=get_lang('launcher.start'), command=self.start_game)
        self.exit_button = ttk.Button(self, text=get_lang('launcher.exit'),  command=lambda: exit())
        self.game_item_list = Listbox(self, height=12)
        self.vscroll = ttk.Scrollbar(self, orient='vertical', command=self.game_item_list.yview)
        self.game_item_list.configure(yscrollcommand=self.vscroll.set)
        self.repair_button = ttk.Button(self, text=get_lang('launcher.repair'), command=self.repair)
        self.del_button = ttk.Button(self, text=get_lang('launcher.delete'), command=self.delete)
        self.rename_button = ttk.Button(self, text=get_lang('launcher.rename'), command=self.rename)
        # 显示
        self.new_button.grid(column=0, row=0, padx=5, pady=5)
        self.start_button.grid(column=1, row=0, padx=5, pady=5)
        self.exit_button.grid(column=2, row=0, padx=5, pady=5)
        self.game_item_list.grid(column=0, columnspan=4, row=1, padx=3, pady=5, sticky='news')
        self.vscroll.grid(column=4, row=1, padx=2, pady=5, sticky='nes')
        self.repair_button.grid(column=0, row=2, padx=5, pady=5)
        self.del_button.grid(column=1, row=2, padx=5, pady=5)
        self.rename_button.grid(column=2, row=2, padx=5, pady=5)
        self.resizable(False, False)
        self.refresh()

    def delete(self, event=None):
        # 删除世界
        if self.game_item_list.curselection() == ():
            select = self.game_item_list.get(0)
        else:
            select = self.game_item_list.get(self.game_item_list.curselection()[0])
        if messagebox.askyesno(message=get_lang('launcher.dialog.text.delete') % select,
                title=get_lang('launcher.dialog.title.delete')):
            shutil.rmtree(os.path.join(path['save'], select))
        self.refresh()

    def new(self, event=None):
        # 新的世界对话框
        self.new_dialog = Toplevel(self)
        self.new_dialog.title(get_lang('launcher.dialog.title.new'))
        self.new_dialog_label_name = ttk.Label(self.new_dialog, text=get_lang('launcher.dialog.text.name'))
        self.new_dialog_entry_name = ttk.Entry(self.new_dialog)
        self.new_dialog_label_seed = ttk.Label(self.new_dialog, text=get_lang('launcher.dialog.text.seed'))
        self.new_dialog_entry_seed = ttk.Entry(self.new_dialog)
        self.new_dialog_label_type = ttk.Label(self.new_dialog, text='Type:')
        self.new_dialog_combobox_type = ttk.Combobox(self.new_dialog, values = ('flat', 'random'), width=8)
        self.new_dialog_combobox_type.state(['readonly'])
        self.new_dialog_button_ok = ttk.Button(self.new_dialog,
                text=get_lang('launcher.dialog.text.ok'), command=self.new_world
                                               )
        self.new_dialog_label_name.grid(column=0, row=0, padx=5, pady=5)
        self.new_dialog_entry_name.grid(column=1, row=0, columnspan=2, padx=5,
                                        pady=5)
        self.new_dialog_label_seed.grid(column=0, row=1, padx=5, pady=5)
        self.new_dialog_entry_seed.grid(column=1, row=1, columnspan=2, padx=5,
                                        pady=5)
        self.new_dialog_label_type.grid(column=0, row=2, padx=5, pady=5)
        self.new_dialog_combobox_type.grid(column=1, row=2, pady=5)
        self.new_dialog_button_ok.grid(column=2, row=3, padx=5, pady=5)
        self.new_dialog.resizable(False, False)
        self.new_dialog.geometry('+%d+%d' % (self.winfo_x() + 50,
                                 self.winfo_y() + 50))
        self.new_dialog.transient(self)
        self.new_dialog.deiconify()
        self.new_dialog.grab_set()
        self.new_dialog.wait_window()
        self.new_dialog.mainloop()

    def new_world(self, event=None):
        # 创建一个新的世界
        name = self.new_dialog_entry_name.get()
        seed = s = self.new_dialog_entry_seed.get()
        if seed == '':
            seed = hash(time.ctime())
        else:
            seed = hash(seed)
        if name == '':
            log_err('invalid world name')
        elif s == '_server' and not ([s for s in list(punctuation) if s in name] == []):
            log_err('invalid world name')
        else:
            if not os.path.isdir(os.path.join(path['save'], name)):
                os.mkdir(os.path.join(path['save'], name))
                world = open(os.path.join(path['save'], name, 'world.json'), 'w+')
                world.write('{\n}\n')
                world.close()
                info = {'seed': seed, 'type': self.new_dialog_combobox_type.get(), 'day': 0, 'time': 4}
                json.dump(info, open(os.path.join(path['save'], name, 'info.json'), 'w+'))
                player = {'position': '0.0', 'respawn': '0.0', 'now_block': 0}
                json.dump(player, open(os.path.join(path['save'], name, 'player.json'), 'w+'))
                self.new_dialog.destroy()
                log_info('create world successfully')
        self.refresh()

    def refresh(self):
        # 刷新
        self.game_item_list.delete(0, 'end')
        for item in [i for i in os.listdir(path['save']) if is_game_restore(i)]:
            self.game_item_list.insert('end', item)

    def rename(self):
        # 重命名对话框
        self.rename_dialog = Toplevel(self)
        self.rename_dialog.title(get_lang('launcher.dialog.title.rename'))
        self.rename_dialog_label = ttk.Label(self.rename_dialog,
            style='TLabel', text=get_lang('launcher.dialog.text.name'))
        self.rename_dialog_entry = ttk.Entry(self.rename_dialog)
        name = self.game_item_list.curselection()
        name = self.game_item_list.get(0) if name == () else self.game_item_list.get(name)
        self.rename_dialog_entry.insert(0, name)

        def send_name():
            self.rename_world(name)

        self.old = os.path.join(path['save'], self.rename_dialog_entry.get())
        self.rename_dialog_button = ttk.Button(self.rename_dialog,
                text=get_lang('launcher.dialog.text.ok'), command=send_name)
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

    def rename_world(self, name):
        # 重命名世界
        shutil.move(os.path.join(path['save'], name), os.path.join(path['save'], self.rename_dialog_entry.get()))
        self.rename_dialog.destroy()
        self.refresh()

    def repair(self, event=None):
        select =self.game_item_list.curselection()
        if select == ():
            log_warn('no world selected')
            return
        select = self.game_item_list.get(select[0])
        repair_archive(select)

    def start_game(self, event=None):
        # 启动游戏
        select = self.game_item_list.curselection()
        if  select == ():
            log_warn('no world selected')
            return
        select = self.game_item_list.get(select[0])
        self.destroy()
        try:
            data = load_window()
            game = Game(width=data['width'], height=data['height'], caption='Minecraft', resizable=True)
            game.set_name(select)
            setup()
            pyglet.app.run()
        except SystemExit:
            pass
        except:
            name = '%d.log' % int(time.time())
            log_err('catch error, saved in: log/%s' % name)
            # err_log = open(os.path.join(path['log'], name), 'a+')
            # err_log.write('Minecraft version: %s\n' % VERSION['str'])
            # err_log.write('time: %s\n' % time.ctime())
            # err_log.write('save: %s\n' % select)
            # err_log.write('traceback:\n' + '=' * 34 + '\n')
            traceback.print_exc()
            # err_log.write('=' * 34 + '\n')
            # err_log.flush()
            # err_log.close()
            exit(1)

