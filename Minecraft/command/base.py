from shlex import split

from Minecraft.source import lang
from Minecraft.world.block import blocks
from Minecraft.utils.utils import *


class CommandBase():

    formats = []
    
    def __init__(self, game, position, command):
        self.game = game
        self.position = position
        self.command = command
        self.args = None
        for f in self.formats:
            args = get_args(self.position, command, f)
            if args is not None:
                self.args = args
                break
        if self.args == None:
            self.game.dialogue.add_dialogue('Arguments error')
            raise ValueError

    def run(self):
        pass


def get_pos(n, s):
    try:
        return int(s)
    except:
        if s == '~':
            return int(round(n))
        else:
            if s.startswith('~'):
                try:
                    d = int(s[1:])
                except:
                    return False
                else:
                    return int(round(n + d))
            else:
                return False

def get_args(pos, s, f):
    l = []
    px, py, pz = pos
    command = split(s)[1:]
    if len(command) != len(f):
        return False
    else:
        for item in range(len(f)):
            if f[item] == 'block':
                if command[item] in blocks:
                    l.append(command[item])
                else:
                    return False
            elif f[item] == 'bool':
                if command[item] == 'true':
                    l.append(True)
                elif command[item] == 'false':
                    l.append(False)
                else:
                    return False
            elif f[item] == 'num':
                try:
                    l.append(int(command[item]))
                except:
                    return False
            elif f[item] == 'px':
                pos = get_pos(px, command[item])
                if pos is False:
                    return False
                else:
                    l.append(pos)
            elif f[item] == 'py':
                pos = get_pos(py, command[item]) - 1
                if pos is False:
                    return False
                else:
                    l.append(pos)
            elif f[item] == 'pz':
                pos = get_pos(pz, command[item])
                if pos is False:
                    return False
                else:
                    l.append(pos)
            elif f[item] == 'str':
                l.append(command[item])

        else:
            return l
