from Minecraft.command.base import CommandBase


class GameMode(CommandBase):

    formats = [['num']]
    description = ['Change game mode',
            '/gamemode <number:mode>']

    def run(self):
        if self.args[0] in [0, 1]:
            self.game.player['gamemode'] = self.args[0]
            if self.args[0] == 1:
                self.game.player['flying'] = True
            else:
                self.game.player['flying'] = False

class Say(CommandBase):

    formats = [['str']]
    description = ['Say something',
            '/say <string:str>']

    def run(self):
        self.game.dialogue.add_dialogue(self.args[0])


class Seed(CommandBase):

    formats = [[]]
    description = ['Print the world seed',
            '/seed']

    def run(self):
        self.game.dialogue.add_dialogue('Seed: ' + str(self.game.world.seed))


class SetBlock(CommandBase):

    formats = [['px', 'py', 'pz', 'block']]
    description = ['Place a block',
            '/setblock <position> <block>']

    def run(self):
        self.game.world.add_block(tuple(self.args[:3]), self.args[3])


class Teleport(CommandBase):

    formats = [['px', 'py', 'pz']]

    description = ['Teleport',
            '/tp <position>']

    def run(self):
        self.game.player['position'] = tuple(self.args)


commands = {}
commands['gamemode'] = GameMode
commands['say'] = Say
commands['seed'] = Seed
commands['setblock'] = SetBlock
commands['tp'] = Teleport

class Help(CommandBase):

    formats = [[], ['str']]
    description = ['Show help',
            '/help',
            '/help <string:command>']

    def run(self):
        global commands
        if len(self.args) == 0:
            cmds = ''
            for key, value in commands.items():
                cmds += ' /' + key + '- ' + value.description[0] + '\n'
            self.game.dialogue.add_dialogue(cmds)
        else:
            if self.args[0] in commands:
                cmd = commands[self.args[0]]
                self.game.dialogue.add_dialogue('\n'.join(cmd.description[1:]))

commands['help'] = Help
