from Minecraft.command.base import CommandBase


class Say(CommandBase):

    formats = [['str']]

    def run(self):
        self.game.dialogue.add_dialogue(self.args[0])


class SetBlock(CommandBase):

    formats = [['px', 'py', 'pz', 'block']]

    def run(self):
        self.game.world.add_block(tuple(self.args[:3]), self.args[3])


commands = {}
commands['say'] = Say
commands['setblock'] = SetBlock
