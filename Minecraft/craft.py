# Minecraft 合成系统
# 合成系统由 craft.json 来控制, 关键字如下:
# item  合成物品名
# tabel 合成表, 有 2*2 和 3*3两种格式, 以空格分隔:
#       "table": [
#           ["x x"], 
#           ["x x"]
#        ]
# need  所需材料: {"x": "plank"}
# times 合成后的数量

import json

class Craft(object):
    
    def __init__(self):
        self.table = {}
        table = jaon.load(open('resource/json/craft.json'))['craft']
        self._set(table)

    def _set(self, table):
        for item in table:
            self.table[item['item']] = CraftItem(item['table'], item['need'], item['times'])

class CraftItem(object):

    def __init__(self, table, need, times):
        self.table = table
        self.need = need
        self.times = times

    def isitem(table):
        pass
