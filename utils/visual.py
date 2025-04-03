import os
import sys
import threading
import time
import platform

#from utils.music_player import MusicPlayer


class ActualSong:
    def __init__(self, name, artist, duration, play_time, album):
        self.name = name            # 'Beat It'
        self.artist = artist        # 'Michael Jackson'
        self.duration = duration    # 258
        self.time = play_time       # 5
        self.album = album          # 'Thriller'



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

    def print_line(self, text, text_color, border_color):
        "---------Row print---------"
        """print(border_color, end='')
        print('┃', end='')
        print(Colors.reset, end='')

        print(text_color, end='')
        print(text.ljust(self.__window_width - 2, ' '), end='')
        print(Colors.reset, end='')

        print(border_color, end='')
        print('┃', end='')
        print(Colors.reset, end='')"""
        "---------Row print---------"
        line_string = (f"{border_color}┃"
                       f"{text_color}{text.ljust(self.__window_width - 2, ' ')}"
                       f"{border_color}┃{Colors.reset}")
        print(line_string)


    def print_box_start(self, text, border_color):
        "---------Start row print---------"
        """print(border_color, end='')
        print('┏╸' + f'{text}╺'.ljust(self.__window_width - 3, '━') + '┓')
        print(Colors.reset, end='')"""
        "---------Start row print---------"
        line_string = f"{border_color}┏╸{text}╺{'━'*(self.__window_width - 3 - len(text) - 1)}┓{Colors.reset}"
        print(line_string)

    def print_box_end(self, border_color):
        "---------End row print---------"
        """print(border_color,end='')
        print('┗'+'━'* (self.__window_width - 2) +'┛')
        print(Colors.reset,end='')"""
        "---------End row print---------"
        line_string = f"{border_color}┗{'━' * (self.__window_width - 2)}┛{Colors.reset}"
        print(line_string)

    def song_bar(self, actual_time, duration, border_color, text, secondary):
        line_len = 30

        print(border_color, end='')
        print('┃', end='')
        print(Colors.reset, end='')

        perc = int(actual_time / (duration / line_len))

        print(text, end='')
        print('[' , end='')
        print(Colors.reset, end='')

        print(secondary, end='')
        print('─' * perc + '│', end='')
        print(Colors.reset, end='')

        print(text, end='')
        print('─' * (line_len-perc) + ']', end='')
        print(Colors.reset, end='')

        actual_time_min = f"{actual_time//60}:{str((actual_time%60)).rjust(2,'0')}"
        duration_min = f"{duration//60}:{str(duration%60).rjust(2,'0')}"

        print(Colors.bold, end='')
        print(' '*10 + f"[{actual_time_min}/{duration_min}]".ljust(20) + ' '*15, end='')
        print(Colors.reset, end='')


        print(border_color, end='')
        print('┃', end='')
        print(Colors.reset, end='')
        print()

    def auto_resize(self):
        size = os.get_terminal_size()
        if size[0] == self.__window_width and size[1] == self.__window_height:
            return

        plt = platform.system()
        if plt == 'Darwin':
            os.system(f"printf \'\e[8;{self.__window_height};{self.__window_width}t\'")
        elif plt == 'Windows':
            os.system(f"mode con: cols={self.__window_width} lines={self.__window_height}")

    def update(self, song: ActualSong):
        # print(' Music player - v1')

        if self.do_autoresize:
            self.auto_resize()

        self.print_box_start('Queue', self.tertiary_fg_color)

        self.print_line('ID   Title' + ' ' * 30 + 'Artist' + ' ' * 20 + 'Duration', self.secondary_fg_color,
                        self.tertiary_fg_color)

        for _ in range(11):
            self.print_line(' ', self.primary_fg_color, self.tertiary_fg_color)

        self.print_box_end(self.tertiary_fg_color)

        self.print_box_start('Playing', self.primary_fg_color)

        self.print_line(song.name, self.tertiary_fg_color, self.primary_fg_color)
        self.print_line(f"{song.artist} - {song.album}", self.secondary_fg_color, self.primary_fg_color)
        self.song_bar(song.time, song.duration, self.primary_fg_color, self.primary_fg_color, self.tertiary_fg_color)
        self.print_box_end(self.primary_fg_color)

    def main(self):
        new_song = ActualSong('Beat It', 'Michael Jackson', 258, 3, 'Thriller')

        for i in range(258 + 1):
            start = time.process_time()
            self.update(new_song)
            end = time.process_time()
            time.sleep(1+start-end)
            #time.sleep(1)
        pass


"========================================================================================================="

os.system('clear')
vis = Visuals()

vis.main()

time.sleep(100)
