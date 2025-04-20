__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "18/04/2025"
__created__ = "03/03/2025"

"""
Filename: visual.py
"""

import os
import time
import platform

from utils.classes import Colors


class Visuals:
    def __init__(self):
        self.__window_height = 20   # height of console window
        self.__window_width = 80    # width of console window
        self.primary_fg_color = Colors.reset    # primary color of console window
        self.secondary_fg_color = Colors.bold   # secondary color of console window
        self.tertiary_fg_color = Colors.Fg.light_cyan   # tertiary color of console window

        self.history_queue = None   # queue of songs that already played
        self.current_song = None    # currently playing song
        self.upcoming_queue = None  # queue of songs that are going to be played

        self.do_autoresize = True   #
        self.fps = 10               #

        self.actual_string = ''
        self.last_string = ''

        self.id_max_len = 2

    def print_line(self, text, text_color, border_color):
        line_string = (f"{border_color}┃"
                       f"{text_color}{text.ljust(self.__window_width - 2, ' ')}"
                       f"{border_color}┃{Colors.reset}\n")
        self.actual_string += line_string

    def print_box_start(self, text, border_color):
        line_string = f"{border_color}┏╸{text}╺{'━'*(self.__window_width - 3 - len(text) - 1)}┓{Colors.reset}\n"
        self.actual_string += line_string

    def print_box_end(self, border_color):
        line_string = f"{border_color}┗{'━' * (self.__window_width - 2)}┛{Colors.reset}\n"
        self.actual_string += line_string

    def print_song_line(self, song, s_id, prim=None):
        if prim is None:
            prim = self.primary_fg_color

        # TODO: add visualization for hours (playlists longer than hour)
        # TODO: add check for characters in name (only some list of ASCII allowed)

        name_len = 56

        song_id = str(s_id)[:self.id_max_len]
        name = song.name[:name_len]
        duration = song.duration

        line = f" {song_id.rjust(self.id_max_len, ' ')}{' '*2}{name.ljust(name_len, ' ')}{' ' * 5}[{duration // 60}:{str(duration % 60).rjust(2, '0')}]"
        self.print_line(line, prim, self.tertiary_fg_color)

    def print_queue_list(self):
        """
        :return:

            printing:
                '
        """
        printed = 1

        h_nums = 5
        if len(self.history_queue) < h_nums:
            h_nums = len(self.history_queue)

        for i in range(h_nums):
            self.print_song_line(self.history_queue.queue[(h_nums-1) - i], printed)
            printed += 1

        self.print_song_line(self.current_song, printed, self.secondary_fg_color)
        printed += 1

        u_nums = 5 + (5-h_nums)
        if len(self.upcoming_queue) < u_nums:
            u_nums = len(self.upcoming_queue)

        for i in range(u_nums):
            self.print_song_line(self.upcoming_queue.queue[i], printed)
            printed += 1

        for i in range(11-printed):
            self.print_line('', self.primary_fg_color, self.tertiary_fg_color)

    def song_bar(self, actual_time, duration, border_color, text, secondary):
        """
        :param actual_time:
        :param duration:
        :param border_color:
        :param text:
        :param secondary:
        :return:

            printing:
                '[────────────────────────────│──]          [3:38/3:51]'
        """
        line_len = 30

        perc = int(actual_time / (duration / line_len))
        actual_time_min = f"{actual_time // 60}:{str((actual_time % 60)).rjust(2, '0')}"
        duration_min = f"{duration // 60}:{str(duration % 60).rjust(2, '0')}"

        line_string = (f"{border_color}┃{text}[{secondary}{'─' * perc}│{text}{'─' * (line_len-perc)}]"
                       f"{Colors.bold}{' '*10}{('['+actual_time_min+'/'+duration_min+']').ljust(20)}{' '*15}{border_color}┃{Colors.reset}\n")
        self.actual_string += line_string

    def set_cmd_size(self):
        plt = platform.system()

        if plt == 'Darwin':
            os.system(f"printf \'\e[8;{self.__window_height};{self.__window_width}t\'")
        elif plt == 'Windows':
            os.system(f"mode con: cols={self.__window_width} lines={self.__window_height}")

    def auto_resize(self):
        size = os.get_terminal_size()
        if size[0] != self.__window_width or size[1] != self.__window_height:
            self.set_cmd_size()

    def update(self, current_song, history_queue, upcoming_queue):

        self.current_song = current_song
        self.history_queue = history_queue
        self.upcoming_queue = upcoming_queue

        self.actual_string = '\n'

        if self.do_autoresize:
            self.auto_resize()

        self.print_box_start('Queue', self.tertiary_fg_color)

        self.print_line('ID:' + ' '*self.id_max_len + 'Title:' + ' ' * 30 + 'Artist:' + ' ' * 20 + 'Duration:', self.secondary_fg_color,
                        self.tertiary_fg_color)

        self.print_queue_list()

        self.print_box_end(self.tertiary_fg_color)

        self.print_box_start('Playing', self.primary_fg_color)

        self.print_line(self.current_song.name, self.tertiary_fg_color, self.primary_fg_color)
        self.print_line(f"{self.current_song.artist}", self.secondary_fg_color, self.primary_fg_color)
        self.song_bar(self.current_song.time, self.current_song.duration, self.primary_fg_color, self.primary_fg_color, self.tertiary_fg_color)
        self.print_box_end(self.primary_fg_color)

        if self.last_string != self.actual_string:
            print(self.actual_string, end='')
            self.last_string = self.actual_string

    def main(self, music_player):
        while True:
            start_update = time.process_time()

            music_player.handle_event()
            self.update(music_player.current_song, music_player.history_queue, music_player.upcoming_queue)

            end_update = time.process_time()

            if end_update - start_update < 1 / self.fps:
                time.sleep(1 / self.fps - (end_update - start_update))

    def print_logo(self):
        for _ in range(2):
            print()

        offset = 20
        with open('data/logo', 'r') as file:
            for line in file.readlines():
                print(' ' * offset + line, end='')

        for _ in range(1):
            print()

"========================================================================================================="

if __name__ == '__main__':
    pass

