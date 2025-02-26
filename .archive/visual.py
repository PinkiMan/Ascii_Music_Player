import os
import sys
import threading
import time


os.system('clear')
os.system('mode con: cols=80 lines=20')

class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
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
        self.primary_fg_color = colors.reset
        self.secondary_fg_color = colors.bold
        self.tertiary_fg_color = colors.fg.lightcyan

    def print_line(self, text, text_color, border_color):
        "---------Row print---------"
        print(border_color, end='')
        print('┃', end='')
        print(colors.reset, end='')

        print(text_color, end='')
        print(text.ljust(78, ' '), end='')
        print(colors.reset, end='')

        print(border_color, end='')
        print('┃', end='')
        print(colors.reset, end='')
        "---------Row print---------"

    def print_box_start(self, text, border_color):
        "---------Start row print---------"
        print(border_color, end='')
        print('┏╸' + f'{text}╺'.ljust(77, '━') + '┓')
        print(colors.reset, end='')
        "---------Start row print---------"

    def print_box_end(self, border_color):
        "---------End row print---------"
        print(border_color,end='')
        print('┗'+'━'*78+'┛')
        print(colors.reset,end='')
        "---------End row print---------"

    def song_bar(self, actual_time, duration, border_color, text, secondary):
        line_len = 30

        print(border_color, end='')
        print('┃', end='')
        print(colors.reset, end='')

        perc = int(actual_time / (duration / line_len))

        print(text, end='')
        print('[' , end='')
        print(colors.reset, end='')

        print(secondary, end='')
        print('─' * perc + '│', end='')
        print(colors.reset, end='')

        print(text, end='')
        print('─' * (line_len-perc) + ']', end='')
        print(colors.reset, end='')

        actual_time_min = f"{actual_time//60}:{actual_time%60}"
        duration_min = f"{duration//60}:{duration%60}"

        print(colors.bold, end='')
        print(' '*10 + f"[{actual_time_min}/{duration_min}]".ljust(20) + ' '*15, end='')
        print(colors.reset, end='')


        print(border_color, end='')
        print('┃', end='')
        print(colors.reset, end='')

    def update(self):
        actual_song_name = 'Beat It'
        actual_song_artist = 'Michael Jackson'
        actual_song_duration = 258
        actual_song_time = 150
        actual_song_album = 'Thriller'

        # print(' Music player - v1')

        # os.system('cls')
        os.system('mode con: cols=80 lines=20')

        self.print_box_start('Queue', self.tertiary_fg_color)

        self.print_line('ID   Title' + ' ' * 30 + 'Artist' + ' ' * 20 + 'Duration', self.secondary_fg_color,
                        self.tertiary_fg_color)

        for _ in range(11):
            self.print_line(' ', self.primary_fg_color, self.tertiary_fg_color)

        self.print_box_end(self.tertiary_fg_color)

        self.print_box_start('Playing', self.primary_fg_color)

        self.print_line(actual_song_name, self.tertiary_fg_color, self.primary_fg_color)
        self.print_line(f"{actual_song_artist} - {actual_song_album}", self.secondary_fg_color, self.primary_fg_color)
        self.song_bar(actual_song_time, actual_song_duration, self.primary_fg_color, self.primary_fg_color, self.tertiary_fg_color)

        self.print_box_end(self.primary_fg_color)

    def main(self):
        self.update()
        pass


"========================================================================================================="


vis = Visuals()

vis.main()

time.sleep(100)
