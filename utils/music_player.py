__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "18/04/2025"
__created__ = "06/02/2025"

"""
Filename: music_player.py
"""

import pygame
import os
import sys
import time
import datetime

from utils.classes import Queue, ActualSongObject, SongLibrary


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        self.history_queue = Queue()
        self.current_song = ActualSongObject().empty()
        self.upcoming_queue = Queue()

        self.volume = 0.01
        self.paused = False

        self.library = SongLibrary()
        self.recommender = None

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

            if self.current_song.name != 'Empty song':
                self.library.write_song_played(self.current_song)

            self.current_song = self.upcoming_queue.pop()
            self.current_song.start_datetime = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S')

            pygame.mixer.music.load(os.path.join(self.library.song_directory, self.current_song.filename))
            pygame.mixer.music.play()
            #print(f'Hraje: {self.current_song.name}')
        else:
            pass
            #print('Fronta je prázdná!')

    def previous_song(self):
        self.history_queue.add(self.current_song)

        self.current_song = self.history_queue.last()
        pygame.mixer.music.load(os.path.join(self.library.song_directory, self.current_song.filename))
        pygame.mixer.music.play()
        #print(f'Předchozí píseň: {self.current_song.name}')


    def handle_event(self):
        self.current_song.time = int(self.__get_time())

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.next_song()

                return True
        return False


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
                self.current_song.skip_at_time = int(self.__get_time())
                self.current_song.skip_datetime = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S')
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

