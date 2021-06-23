import random

from minecraft.command.base import CommandBase
from minecraft.command.arguments import *
from minecraft.source import resource_pack
from minecraft.world.sky import change_sky_color
from minecraft.world.weather import weather

commands = {}


class CommandGameMode(CommandBase):

    formats = [ArgumentCollection(mode=NumberArgument())]
    description = [resource_pack.get_translation('command.name.gamemode.help'),
            '/gamemode <number:mode>'
        ]

    def execute(self):
        if self.args['mode'] in [0, 1]:
            self.game.player['gamemode'] = self.args['mode']
            if self.args[0] == 1:
                self.game.player['flying'] = True
            else:
                self.game.player['flying'] = False


class CommandHelp(CommandBase):

    formats = [ArgumentCollection(),
            ArgumentCollection(cmd=StringArgument())]
    description = [resource_pack.get_translation('command.name.help.help'),
            '/help',
            '/help <string:command>'
        ]

    def execute(self):
        global commands
        if len(self.args) == 0:
            cmds = ''
            for key, value in commands.items():
                cmds += '/' + key + ' - ' + value.description[0] + '\n'
            self.game.dialogue.add_dialogue(cmds)
        elif 'cmd' in self.args:
            cmd = commands[self.args['cmd']]
            self.game.dialogue.add_dialogue('\n'.join(cmd.description[1:]))


class CommandSay(CommandBase):

    formats = [ArgumentCollection(text=StringArgument())]
    description = [resource_pack.get_translation('command.name.say.help'),
            '/say <string:str>'
        ]

    def execute(self):
        self.game.dialogue.add_dialogue(self.args['text'])


class CommandSeed(CommandBase):

    formats = [ArgumentCollection()]
    description = [resource_pack.get_translation('command.name.seed.help'),
            '/seed'
        ]

    def execute(self):
        self.game.dialogue.add_dialogue(resource_pack.get_translation('general.seed') + ': ' + str(self.game.world.seed))


class CommandSetBlock(CommandBase):

    formats = [ArgumentCollection(x=PositionArgument('x'), y=PositionArgument('y'), z=PositionArgument('z'),
        block=BlockArgument())]
    description = [resource_pack.get_translation('command.name.setblock.help'),
            '/setblock <position> <block>'
        ]

    def execute(self):
        self.game.world.add_block(tuple(self.args['x'], self.args['y'], self.args['z']), self.args['block'])


class CommandTeleport(CommandBase):

    formats = [ArgumentCollection(x=PositionArgument('x'), y=PositionArgument('y'), z=PositionArgument('z'))]
    description = [resource_pack.get_translation('command.name.teleport'),
            '/tp <position>'
        ]

    def execute(self):
        self.game.player['position'] = tuple(self.args.values())


class CommandTime(CommandBase):
    formats = [ArgumentCollection(),
            ArgumentCollection(op=StringArgument('^(add|set)$'), time=NumberArgument(min_=0)),
            ArgumentCollection(op=StringArgument('set'), time=StringArgument('^(day|noon|night)$'))]
    description = [resource_pack.get_translation('command.name.time.help'),
            '/time',
            '/time add <int:second>',
            '/time set <int:time>',
            '/time set <str:day|noon|night>'
        ]

    def execute(self):
        if 'op' not in self.args:
            self.game.dialogue.add_dialogue(str(int(self.game.time)))
        else:
            if self.args['op'] == 'add':
                self.game.time += self.args['time']
            elif self.args['op'] == 'set':
                if isinstance(self.args['time'], int):
                    self.game.time = self.args['time']
                elif isinstance(self.args['time'], str):
                    d = {'day': 300, 'noon': 600, 'night':900}
                    self.game.time = int(self.game.time) // 1200 * 1200 + d[self.args['time']]
            change_sky_color(0)


class CommandWeather(CommandBase):

    formats = [ArgumentCollection(type=StringArgument()),
            ArgumentCollection(type=StringArgument(), duration=NumberArgument(min_=0))]
    description = [resource_pack.get_translation('command.name.weather.help'),
            '/weather <string:type> [int:duration]'
        ]

    def execute(self):
        self.weather = {'now': '', 'duration': 0}
        if self.args['type'] in weather:
            self.weather['now'] = self.args['type']
        else:
            self.game.dialogue.add_dialogue(resource_pack.get_translation('command.name.weather.none_exist') % self.args['type'])
            return
        if 'duration' in self.args:
            duration = weather[self.args['type']].duration
            self.weather['duration'] = min(max(duration[0], self.args['duration']), duration[1])
        else:
            self.weather['duration'] = random.randint(*weather[self.args['type']].duration)
        weather[self.game.weather['now']].leave()
        self.game.weather = self.weather
        weather[self.game.weather['now']].change()


commands['gamemode'] = CommandGameMode
commands['help'] = CommandHelp
commands['say'] = CommandSay
commands['seed'] = CommandSeed
commands['setblock'] = CommandSetBlock
commands['tp'] = CommandTeleport
commands['time'] = CommandTime
commands['weather'] = CommandWeather
