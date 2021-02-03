import random

from Minecraft.command.base import CommandBase
from Minecraft.world.weather import weather


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


class Weather(CommandBase):

    formats = [['str'], ['str', 'int']]
    description = ['Change weather',
            '/weather <string:type> [int:duration]']

    def run(self):
        self.weather = {'now': '', 'duration': 0}
        if self.args[0] in weather:
            self.weather['now'] = self.args[0]
        else:
            self.game.dialogue.add_dialogue("Weather '%s' not exist")
            return
        if len(self.args) == 2:
            duration = weather[self.args[0]].duration
            self.weather['duration'] = min(max(duration[0], self.args[1]), duration[1])
        else:
            self.weather['duration'] = random.randint(*weather[self.args[0]].duration)
        weather[self.game.weather['now']].leave()
        self.game.weather = self.weather
        weather[self.game.weather['now']].change()


commands = {}
commands['gamemode'] = GameMode
commands['say'] = Say
commands['seed'] = Seed
commands['setblock'] = SetBlock
commands['tp'] = Teleport
commands['weather'] = Weather

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
                cmds += ' /' + key + ' - ' + value.description[0] + '\n'
            self.game.dialogue.add_dialogue(cmds)
        else:
            if self.args[0] in commands:
                cmd = commands[self.args[0]]
                self.game.dialogue.add_dialogue('\n'.join(cmd.description[1:]))

commands['help'] = Help
