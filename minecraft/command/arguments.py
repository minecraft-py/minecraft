import re
from shlex import split

from minecraft.source import resource_pack
from minecraft.block import blocks
from minecraft.utils.utils import *


class BaseArgument:

    def __init__(self):
        pass

    def valid(self, value):
        pass


class StringArgument(BaseArgument):

    def __init__(self, expr=None):
        super().__init__()
        self.re_expr = expr

    def valid(self, value):
        if self.re_expr:
            if re.match(self.re_expr, value):
                return value
            else:
                raise TypeError(resource_pack.get_translation('command.args.string.not_available') % value)
        else:
            return value


class NumberArgument(BaseArgument):

    def __init__(self, type_=int, min_=None, max_=None):
        super().__init__()
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
                    return value
            elif self.range[0] is not None:
                if self.range[0] <= value:
                    return value
            elif self.range[1] is not None:
                if self.range[1] >= value:
                    return value
            else:
                return value
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

    def __init__(self):
        super().__init__()

    def valid(self, value):
        if value in blocks:
            return value
        else:
            raise TypeError(resource_pack.get_translation('command.args.block.wrong') % value)

class BooleanArgument(BaseArgument):

    def __init__(self):
        super().__init__()

    def valid(self, value):
        if value == 'true':
            return True
        elif value == 'false':
            return False
        else:
            raise TypeError(resource_pack.get_translation('command.args.boolean.wrong') % value)


class PositionArgument(BaseArgument):

    def __init__(self, axis):
        super().__init__()
        self.axis = axis

    def valid(self, value):
        try:
            return int(value) - (1 if self.axis == 'y' else 0)
        except:
            if value.startswith('~'):
                if value == '~':
                    return int(round(get_game().player['position'][ord(self.axis) - 120])) - (1 if self.axis == 'y' else 0)
                try:
                    delta = int(value[1:]) - (1 if self.axis == 'y' else 0)
                except:
                    raise TypeError(resource_pack.get_translation('command.args.position.wrong') % value)
                else:
                    return (int(round(get_game().player['position'][ord(self.axis) - 120] + delta)) -
                            (1 if self.axis == 'y' else 0))
            else:
                raise TypeError(resource_pack.get_translation('command.args.position.wrong') % value)


class DictArgument(BaseArgument):

    def __init__(self, argument):
        super().__init__()
        if isinstance(arg, DictArgument):
            # 禁止套娃
            raise RecursionError()
        else:
            self.argument = argument

    def valid(self, value):
        pass


class ArgumentCollection():

    def __init__(self, **args):
        self.args = args

    def valid(self, cmd):
        args = dict()
        cmdargs = split(cmd)[1:]
        if len(cmdargs) != len(self.args):
            return False
        else:
            count = 0
            for key, value in self.args.items():
                args.setdefault(str(key), value.valid(cmdargs[count]))
                count += 1
            else:
                return args
