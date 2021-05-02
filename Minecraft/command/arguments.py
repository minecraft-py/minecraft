import re

from Minecraft.world.block import blocks


class BaseArgument:

    def __init__(self):
        pass

    def valid(self, value):
        pass


class StringArgument(BaseArgument):

    def __init__(self, name, expr='*'):
        super().__init__(self)
        self.name = str(name)
        self.re_expr = expr

    def valid(self, value):
        if re.match(self.re_expr, value):
            return {self.name: self.string}
        else:
            raise TypeError()


class NumberArgument(BaseArgument):

    def __init__(self, name, type_=int, min_=None, max_=None):
        super().__init__(self)
        self.name = str(name)
        self.type = (min_, max_)
        self.range = range_

    def valid(self, value):
        try:
            value = self.type(value)
        except:
            raise TypeError()
        else:
            if (self.type[0] is not None) and (self.type[1] is not None):
                if self.type[0] <= value <= self.type[1]:
                    return {self.name: value}
            elif self.type[0] is not None:
                if self.type[0] <= value:
                    return {self.name: self.value}
            elif self.type[1] is not None:
                if self.type[1] is not None:
                    if self.type[1] >= value:
                        return {self.name: value}
            raise TypeError()


def BlockArgument(BaseArgument):

    def __init__(self, name):
        super().__init__(self)
        self.name = str(name)

    def valid(self, value):
        if value in blocks:
            return {self.name: value}
        else:
            raise TypeError()

class BooleanArgument(BaseArgument):

    def __init__(self, name):
        super().__init__(self)
        self.name = str(name)

    def valid(self):
        if self.value == 'true':
            return {self.name: True}
        elif self.value == 'false':
            return {self.name: False}
        else:
            raise TypeError()


class ArgumentCollection():

    def __init__(self, *args):
        pass
