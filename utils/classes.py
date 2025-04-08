__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "08/04/2025"
__created__ = "03/04/2025"

"""
Filename: classes.py
"""

import os

class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        light_grey = '\033[37m'
        darkgrey = '\033[90m'
        light_red = '\033[91m'
        light_green = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'

class Queue:
    def __init__(self):
        self.queue = []

    def insert(self, item):
        self.queue.insert(0, item)

    def add(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0)

    def last(self):
        return self.queue[0]

    def __len__(self):
        return len(self.queue)

class ActualSong:
    def __init__(self):
        self.name = ''  # 'Beat It'
        self.artist = ''  # 'Michael Jackson'
        self.duration = -1  # 258
        self.time = -1  # 5
        self.album = ''  # 'Thriller'
        self.filepath = ''

    def create_from_filename(self, filepath):
        self.filepath = filepath
        self.name = '.'.join(os.path.basename(filepath).split('.')[:-1])

    def empty(self):
        self.name = 'Empty song'

        return self


