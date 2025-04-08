__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "08/04/2025"
__created__ = "06/02/2025"

"""
Filename: music_player.py
"""

import pygame
import os
import sys
import time

from utils.classes import Queue, ActualSong


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.history_queue = Queue()
        self.current_song = ActualSong().empty()
        self.upcoming_queue = Queue()

        self.volume = 0.1
        self.paused = False

        pygame.mixer.music.set_volume(self.volume)

    def __is_playing(self):
        return pygame.mixer.music.get_busy()

    def __get_time(self):
        return pygame.mixer.music.get_pos()/1000

    def play(self):
        if self.paused:
            self.resume()
        else:
            self.next_song()
            #print('Pokračuje se v přehrávání')

    def resume(self):
        pygame.mixer.music.unpause()
        #print('Odpauzovano')

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True
        #print('Pozastaveno')

    def stop(self):
        pygame.mixer.music.stop()
        #print('Zastaveno')

    def set_volume(self, setting):
        pygame.mixer.music.set_volume(setting)

    def add_to_queue(self, song):
        self.upcoming_queue.add(song)
        #print(f'Přidáno do fronty: {song.name}')

    def next_song(self):
        if len(self.upcoming_queue) > 0:
            self.history_queue.insert(self.current_song)

            self.current_song = self.upcoming_queue.pop()
            pygame.mixer.music.load(self.current_song.filepath)
            pygame.mixer.music.play()
            #print(f'Hraje: {self.current_song.name}')
        else:
            pass
            #print('Fronta je prázdná!')

    def previous_song(self):
        self.history_queue.add(self.current_song)

        self.current_song = self.history_queue.last()
        pygame.mixer.music.load(self.current_song.filepath)
        pygame.mixer.music.play()
        #print(f'Předchozí píseň: {self.current_song.name}')


    def handle_event(self):
        self.current_song.time = int(self.__get_time())

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.next_song()

                return True
        return False


    def print_queue(self):
        nums = 5

        history_nums = nums if len(self.history_queue) else len(self.history_queue)
        upcoming_nums = nums if len(self.upcoming_queue) else len(self.upcoming_queue)

        names = []

        for i in range(history_nums):
            names.append(f"{-history_nums+len(names)} - {self.history_queue.queue[i].name}")

        names.append(f" {-history_nums+len(names)} - {self.current_song.name}")

        for i in range(upcoming_nums):
            names.append(f"+{-history_nums+len(names)} - {self.upcoming_queue.queue[i].name}")

        return '\n'.join(names)

    def exit(self):
        pygame.mixer.quit()
        pygame.quit()

    def get_user_input(self):
        running = True
        while running:
            command = input('> ').strip().lower()
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")

            if command == "play":
                self.play()
            elif command == "pause":
                self.pause()
            elif command == "stop":
                self.stop()
            elif command == "next":
                self.next_song()
                time.sleep(1)
            elif command == "shuffle":
                self.shuffle_queue()
            elif command == "exit":
                self.exit()
                break
            else:
                pass
                #print("Neznámý příkaz!")

