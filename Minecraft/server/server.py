import random
import sys

from Minecraft.utils.utils import *


class Server():

    def __init__(self, save):
        self._save = save

    def start(self):
        log_info('Start built-in server', 'server')
        while True:
            if sys.is_finalizing():
                log_info('Shutdown built-in server', 'server')
                return
