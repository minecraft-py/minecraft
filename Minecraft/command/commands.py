import random

from Minecraft.command.base import CommandBase
from Minecraft.world.sky import change_sky_color
from Minecraft.world.weather import weather

commands = {}


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


class Help(CommandBase):

    formats = [[], ['int'], ['str']]
    description = ['Show help',
            '/help',
            '/help <int:page>',
            '/help <string:command>']

    def run(self):
        global commands
        if len(self.args) == 0:
            cmds = ''
            for key, value in commands.items():
                cmds += '/' + key + ' - ' + value.description[0] + '\n'
            self.game.dialogue.add_dialogue(cmds)
        else:
            if self.args[0] in commands:
                cmd = commands[self.args[0]]
                self.game.dialogue.add_dialogue('\n'.join(cmd.description[1:]))


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


class Time(CommandBase):
    formats = [[], ['str', 'int'], ['str', 'str']]
    description = ['Get or set the time',
            '/time',
            '/time add <int:second>',
            '/time set <int:time>',
            '/time set <str:day|noon|night>']

    def run(self):
        if len(self.args) == 0:
            self.game.dialogue.add_dialogue(str(int(self.game.time)))
        else:
            if self.args[0] == 'add':
                if isinstance(self.args[1], int):
                    self.game.time += max(0, self.args[1])
                else:
                    self.game.dialogue.add_dialogue("'%s' not a number" % self.args[1])
            elif self.args[0] == 'set':
                if isinstance(self.args[1], int):
                    self.game.time = max(0, self.args[1])
                elif isinstance(self.args[1], str):
                    d = {'day': 300, 'noon': 600, 'night':900}
                    if self.args[1] not in d:
                        self.game.dialogue.add_dialogue("Unknow time : '%s'" % self.args[1])
                    else:
                        self.game.time = int(self.game.time) // 1200 * 1200 + d[self.args[1]]
                change_sky_color(0)
            else:
                self.game.dialogue.add_dialogue("Unknow sub command: '%s'" % self.args[0])


class Weather(CommandBase):

    formats = [['str'], ['str', 'int']]
    description = ['Change weather',
            '/weather <string:type> [int:duration]']

    def run(self):
        self.weather = {'now': '', 'duration': 0}
        if self.args[0] in weather:
            self.weather['now'] = self.args[0]
        else:
            self.game.dialogue.add_dialogue("Weather '%s' not exist" % self.args[0])
            return
        if len(self.args) == 2:
            duration = weather[self.args[0]].duration
            self.weather['duration'] = min(max(duration[0], self.args[1]), duration[1])
        else:
            self.weather['duration'] = random.randint(*weather[self.args[0]].duration)
        weather[self.game.weather['now']].leave()
        self.game.weather = self.weather
        weather[self.game.weather['now']].change()


commands['gamemode'] = GameMode
commands['help'] = Help
commands['say'] = Say
commands['seed'] = Seed
commands['setblock'] = SetBlock
commands['tp'] = Teleport
commands['time'] = Time
commands['weather'] = Weather
