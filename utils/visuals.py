import os
import sys
import threading
import time

from utils.music_player import Queue, MusicPlayer


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
        self.player = MusicPlayer()


    def get_user_input(self):
        running = True
        while running:
            command = input('> ').strip().lower()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

            if command == "play":
                self.player.play()
            elif command == "pause":
                self.player.pause()
            elif command == "stop":
                self.player.stop()
            elif command == "next":
                self.player.next_song()
                self.update()
                time.sleep(1)
            elif command == "shuffle":
                self.player.shuffle_queue()
            elif command == "exit":
                self.player.exit()
                break
            else:
                pass
                #print("Neznámý příkaz!")

    def print_queue(self):
        nums = 5

        history_nums = nums if len(self.player.history_queue) > nums else len(self.player.history_queue)
        upcoming_nums = nums if len(self.player.upcoming_queue) > nums else len(self.player.upcoming_queue)

        printed = 0

        for i in range(nums - history_nums):
            print('-')
            printed += 1


        for i in range(history_nums):
            print(f"{-nums + printed} - {self.player.history_queue.queue[nums - printed - 1].name}")
            printed += 1

        print(colors.bold, colors.fg.yellow,f" {printed - nums} - {self.player.current_song.name}", colors.reset)
        printed += 1

        for i in range(upcoming_nums):
            print(f"+{printed - nums} - {self.player.upcoming_queue.queue[i].name}")
            printed += 1

    def update(self):
        os.system('cls')
        os.system('mode con: cols=80 lines=20')

        print('-----Music player-----')
        print()

        self.print_queue()

        print()
        print()

        print('Now playing:\t\t\t\t\t\t\tVolume:')
        print(' - ' + self.player.current_song.name[0:60].ljust(63) + '- ' + str(self.player.volume * 100) + '%')
        print()

    def main_loop(self):
        threading.Thread(target=self.get_user_input, daemon=True).start()

        while True:
            new_song = self.player.handle_event()

            if new_song:
                self.update()




"""Quit = False
Paused=False
while not Quit:
    Input = input('> ')
    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")


    Input=Input.split(' ')


    if Input[0] == "Quit" or Input[0]=="q" or Input[0]=="quit":     #exit
        Quit = True

    elif Input[0]=="p":     #pause / unpause
        if Paused:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()

            Paused=True

    elif Input[0]=='v':     #volume
        if len(Input)==2:
            VOLUME=float(Input[1])/100
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
            print()
            pygame.mixer.music.set_volume(VOLUME)
        elif len(Input)==1:
            VOLUME = 0.125
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
            print()
            pygame.mixer.music.set_volume(VOLUME)

    elif Input[0]=='stop':      #stop
        pygame.mixer.music.stop()
        NOW_PLAYING=''
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")
        print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
        print()

    elif Input[0]=='reset':     #reset view
        os.system('mode con: cols=80 lines=20')
        print('-----Music player-----')
        print()

        print_songs(All_Songs,0)

        for _ in range(4):
            print()

        print('Now playing:\t\t\t\t\t\t\tVolume:')
        print(' - ' + INIT_SONG[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
        print()

    else:
        try:
            num=int(Input[0])
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            NOW_PLAYING=All_Songs[num-1]
            print(' - '+NOW_PLAYING[0:60].ljust(63)+'- '+str(VOLUME*100)+'%')
            print()
            Play_Song(All_Songs[num-1],num)


        except:
            pass"""