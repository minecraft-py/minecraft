import re
from shlex import split

from Minecraft.world.block import blocks


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
                raise TypeError()
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
            raise TypeError()
        else:
            if (self.range[0] is not None) and (self.range[1] is not None):
                if self.range[0] <= value <= self.range[1]:
                    return {self.name: value}
            elif self.range[0] is not None:
                if self.range[0] <= value:
                    return {self.name: value}
            elif self.range[1] is not None:
                if self.range[1] is not None:
                    if self.range[1] >= value:
                        return {self.name: value}
            else:
                return {self.name: value}
            raise TypeError()


class BlockArgument(BaseArgument):

    def __init__(self, name):
        super().__init__()
        self.name = str(name)

    def valid(self, value):
        if value in blocks:
            return {self.name: value}
        else:
            raise TypeError()

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
            raise TypeError()


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
                try:
                    delta = int(value[1:]) - (1 if self.axis == 'y' else 0)
                except:
                    raise TypeError()
                else:
                    return {self.name: int(round(get_game.player['position'][ord(self.axis) - 120] + delta)) -
                            (1 if self.axis == 'y' else 0)}


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
