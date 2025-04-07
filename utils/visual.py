import os
import sys
import threading
import time
import platform

from utils.music_player import MusicPlayer, ActualSong




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



class Visuals:
    def __init__(self):
        self.__window_height = 20
        self.__window_width = 80
        self.primary_fg_color = Colors.reset
        self.secondary_fg_color = Colors.bold
        self.tertiary_fg_color = Colors.Fg.lightcyan

        self.actual_song = None
        self.queue = []
        self.do_autoresize = True
        self.fps = 10

        self.actual_string = ''


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

    def print_song_line(self, song, id, prim=None):
        if prim is None:
            prim = self.primary_fg_color
        self.print_line(f" {str(id).ljust(5, ' ')}{song.name[:34].ljust(35, ' ')}", prim, self.tertiary_fg_color)

    def print_queue_list(self, history_queue, current_song,  upcoming_queue):
        printed = 1

        h_nums = 5
        if len(history_queue) < h_nums:
            h_nums = len(history_queue)

        for i in range(h_nums):
            self.print_song_line(history_queue.queue[-i - 1], printed)
            printed += 1

        self.print_song_line(current_song, printed, self.secondary_fg_color)
        printed += 1

        u_nums = 5 + (5-h_nums)
        if len(upcoming_queue) < u_nums:
            u_nums = len(upcoming_queue)

        for i in range(u_nums):
            self.print_song_line(upcoming_queue.queue[i], printed)
            printed += 1



    def song_bar(self, actual_time, duration, border_color, text, secondary):
        line_len = 30

        perc = int(actual_time / (duration / line_len))
        actual_time_min = f"{actual_time // 60}:{str((actual_time % 60)).rjust(2, '0')}"
        duration_min = f"{duration // 60}:{str(duration % 60).rjust(2, '0')}"

        line_string = (f"{border_color}┃{text}[{secondary}{'─' * perc}│{text}{'─' * (line_len-perc)}]"
                       f"{Colors.bold}{' '*10}{('['+actual_time_min+'/'+duration_min+']').ljust(20)}{' '*15}{border_color}┃{Colors.reset}\n")
        self.actual_string += line_string

    def auto_resize(self):
        size = os.get_terminal_size()
        if size[0] == self.__window_width and size[1] == self.__window_height:
            return

        plt = platform.system()
        if plt == 'Darwin':
            os.system(f"printf \'\e[8;{self.__window_height};{self.__window_width}t\'")
        elif plt == 'Windows':
            os.system(f"mode con: cols={self.__window_width} lines={self.__window_height}")

    def update(self, song: ActualSong, history_queue,  upcoming_queue):
        # print(' Music player - v1')

        self.actual_string = ''

        if self.do_autoresize:
            self.auto_resize()

        self.print_box_start('Queue', self.tertiary_fg_color)

        self.print_line('ID   Title' + ' ' * 30 + 'Artist' + ' ' * 20 + 'Duration', self.secondary_fg_color,
                        self.tertiary_fg_color)

        self.print_queue_list(history_queue, song, upcoming_queue)
        """for _ in range(11):
            self.print_line(' ', self.primary_fg_color, self.tertiary_fg_color)"""

        self.print_box_end(self.tertiary_fg_color)

        self.print_box_start('Playing', self.primary_fg_color)

        self.print_line(song.name, self.tertiary_fg_color, self.primary_fg_color)
        self.print_line(f"{song.artist} - {song.album}", self.secondary_fg_color, self.primary_fg_color)
        self.song_bar(song.time, song.duration, self.primary_fg_color, self.primary_fg_color, self.tertiary_fg_color)
        self.print_box_end(self.primary_fg_color)


        print(self.actual_string, end='')




"========================================================================================================="

if __name__ == '__main__':
    vis = Visuals()

    new_song = ActualSong()
    new_song.name = 'Beat It'
    new_song.artist = 'Michael Jackson'
    new_song.duration = 258
    new_song.time = 0
    new_song.album = 'Thriller'

    for i in range(258 + 1):
        start = time.process_time()
        new_song.time = i
        vis.update(new_song)
        end = time.process_time()
        time.sleep(1 + start - end)
        # time.sleep(1)
    pass


