import re
from shlex import split

from Minecraft.source import resource_pack
from Minecraft.world.block import blocks
from Minecraft.utils.utils import *


class BaseArgument:

    def __init__(self):
        pass

    def valid(self, value):
        pass


class StringArgument(BaseArgument):

    def __init__(self, name, expr=None):
        super().__init__()
        self.name = str(name)
        self.re_expr = expr

    def valid(self, value):
        if self.re_expr:
            if re.match(self.re_expr, value):
                return {self.name: value}
            else:
                raise TypeError(resource_pack.get_translation('command.args.string.not_available') % value)
        else:
            return {self.name: value}


class NumberArgument(BaseArgument):

    def __init__(self, name, type_=int, min_=None, max_=None):
        super().__init__()
        self.name = str(name)
        self.type = type_
        self.range = (min_, max_)

    def valid(self, value):
        try:
            value = self.type(value)
        except:
            raise TypeError(resource_pack.get_translation('command.args.number.not_a_number') % value)
        else:
            if (self.range[0] is not None) and (self.range[1] is not None):
                if self.range[0] <= value <= self.range[1]:
                    return {self.name: value}
            elif self.range[0] is not None:
                if self.range[0] <= value:
                    return {self.name: value}
            elif self.range[1] is not None:
                if self.range[1] >= value:
                    return {self.name: value}
            else:
                return {self.name: value}
            # 都没有匹配后运行到这里生成错误信息
            if (self.range[0] is not None) and (self.range[1] is not None):
                raise TypeError(resource_pack.get_translation('command.args.number.not_between') % (self.range[0], self.range[1]))
            elif self.range[0] is not None:
                raise TypeError(resource_pack.get_translation('command.args.number.is_small') % (value, self.range[0]))
            elif self.range[1] is not None:
                raise TypeError(resource_pack.get_translation('command.args.number.is_big') % (value, self.range[1]))
            else:
                raise TypeError(resource_pack.get_translation('command.args.number.wrong') % value)


class BlockArgument(BaseArgument):

    def __init__(self, name):
        super().__init__()
        self.name = str(name)

    def valid(self, value):
        if value in blocks:
            return {self.name: value}
        else:
            raise TypeError(resource_pack.get_translation('command.args.block.wrong') % value)

class BooleanArgument(BaseArgument):

    def __init__(self, name):
        super().__init__()
        self.name = str(name)

    def valid(self, value):
        if value == 'true':
            return {self.name: True}
        elif value == 'false':
            return {self.name: False}
        else:
            raise TypeError(resource_pack.get_translation('command.args.boolean.wrong') % value)


class PositionArgument(BaseArgument):

    def __init__(self, name, axis):
        super().__init__()
        self.name = str(name)
        self.axis = axis

    def valid(self, value):
        try:
            return {self.name: int(value) - (1 if self.axis == 'y' else 0)}
        except:
            if value.startswith('~'):
                if value == '~':
                    return {self.name: int(round(get_game().player['position'][ord(self.axis) - 120])) -
                            (1 if self.axis == 'y' else 0)}
                try:
                    delta = int(value[1:]) - (1 if self.axis == 'y' else 0)
                except:
                    raise TypeError(resource_pack.get_translation('command.args.position.wrong') % value)
                else:
                    return {self.name: int(round(get_game().player['position'][ord(self.axis) - 120] + delta)) -
                            (1 if self.axis == 'y' else 0)}
            else:
                raise TypeError(resource_pack.get_translation('command.args.position.wrong') % value)


class DictArgument(BaseArgument):

    def __init__(self, name, argument):
        super().__init__()
        self.name = str(name)
        if isinstance(arg, DictArgument):
            # 禁止套娃
            raise RecursionError()
        else:
            self.argument = argument

    def valid(self, value):
        pass


class ArgumentCollection():

    def __init__(self, *args):
        self.args = args

    def valid(self, cmd):
        args = dict()
        cmdargs = split(cmd)[1:]
        if len(cmdargs) != len(self.args):
            return False
        else:
            for i in range(len(self.args)):
                args.update(self.args[i].valid(cmdargs[i]))
            else:
                return args
