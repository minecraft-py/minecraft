from Minecraft.command.base import CommandBase


class GameMode(CommandBase):

    formats = [['num']]

    def run(self):
        if self.args[0] in [0, 1]:
            self.game.player['gamemode'] = self.args[0]
            if self.args[0] == 1:
                self.game.player['flying'] = True
            else:
                self.game.player['flying'] = False

class Say(CommandBase):

    formats = [['str']]

    def run(self):
        self.game.dialogue.add_dialogue(self.args[0])


class Seed(CommandBase):

    formats = [[]]

    def run(self):
        self.game.dialogue.add_dialogue('Seed: ' + str(self.game.world.seed))


class SetBlock(CommandBase):

    formats = [['px', 'py', 'pz', 'block']]

    def run(self):
        self.game.world.add_block(tuple(self.args[:3]), self.args[3])


class Teleport(CommandBase):

    formats = [['px', 'py', 'pz']]

    def run(self):
        self.game.player['position'] = tuple(self.args)


commands = {}
commands['gamemode'] = GameMode
commands['say'] = Say
commands['seed'] = Seed
commands['setblock'] = SetBlock
commands['tp'] = Teleport
