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
from pynput import keyboard

from utils.classes import Queue, ActualSongObject, SongLibrary
from win32gui import GetWindowText, GetForegroundWindow

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

    def resume(self):
        pygame.mixer.music.unpause()
        self.paused = False

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop(self):
        pygame.mixer.music.stop()

    def set_volume(self, setting):
        pygame.mixer.music.set_volume(setting)

    def add_to_queue(self, song):
        self.upcoming_queue.add(song)

    def next_song(self):
        if len(self.upcoming_queue) > 0:
            self.history_queue.insert(self.current_song)

            if self.current_song.name != 'Empty song':
                self.library.write_song_played(self.current_song)

            self.current_song = self.upcoming_queue.pop()
            self.current_song.start_datetime = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S')

            pygame.mixer.music.load(os.path.join(self.library.song_directory, self.current_song.filename))
            pygame.mixer.music.play()
        else:
            pass

    def previous_song(self):
        self.history_queue.add(self.current_song)

        self.current_song = self.history_queue.last()
        pygame.mixer.music.load(os.path.join(self.library.song_directory, self.current_song.filename))
        pygame.mixer.music.play()

    def handle_event(self):
        new_time = int(self.__get_time())
        if self.current_song.time != new_time:
            self.current_song.time = new_time
            self.current_song.update_visual = True

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
            elif command.split(' ')[0] == 'v':
                self.set_volume(float(command.split(' ')[1])/100)
            else:
                pass

    def on_press(self, key):
        if not str(GetWindowText(GetForegroundWindow())).startswith('Příkazový řádek'):
            return

        if key == keyboard.Key.media_play_pause or key == keyboard.Key.space:
            if self.paused:
                self.play()
            else:
                self.pause()
        elif key == keyboard.Key.media_next:
            self.current_song.skip_at_time = int(self.__get_time())
            self.current_song.skip_datetime = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S')
            self.next_song()
            time.sleep(1)
        elif key == keyboard.Key.media_previous:
            print('previous')
        else:
            if hasattr(key, 'char'):
                if key.char == 'p' or key.char == 'k':
                    self.play()
                elif key.char == 'l':
                    self.current_song.skip_at_time = int(self.__get_time())
                    self.current_song.skip_datetime = datetime.datetime.today().strftime('%d/%m/%Y-%H:%M:%S')
                    self.next_song()
                    time.sleep(1)
                elif key.char == 'j':
                    print('previous')
                elif key.char == '+':
                    self.volume += 0.02
                    self.set_volume(self.volume)
                elif key.char == '-':
                    self.volume -= 0.02
                    self.set_volume(self.volume)

    def get_user_input_2(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()


