from shlex import split

from Minecraft.world.block import blocks
from Minecraft.utils.utils import *


class CommandBase():

    formats = []
    description = ['description.short', 'description.long']
    
    def __init__(self, game, command):
        self.game = game
        self.command = command
        self.args = None
        for item in self.formats:
            args = item.valid(command)
            if args != False:
                self.args = args
                break
        if not isinstance(self.args, dict):
            self.game.dialogue.add_dialogue('Arguments error')
            raise TypeError()

    def execute(self):
        pass

