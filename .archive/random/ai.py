import pygame
import os
from collections import deque


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.queue = deque()
        self.current_song = None
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

    def add_to_queue(self, song_path):
        if os.path.exists(song_path):
            self.queue.append(song_path)
            print(f'Přidáno do fronty: {song_path}')
        else:
            print('Soubor neexistuje!')

    def play(self):
        if not pygame.mixer.music.get_busy():
            self.next_song()
        else:
            pygame.mixer.music.unpause()
            print('Pokračuje se v přehrávání')

    def pause(self):
        pygame.mixer.music.pause()
        print('Pozastaveno')

    def stop(self):
        pygame.mixer.music.stop()
        print('Zastaveno')

    def next_song(self):
        if self.queue:
            self.current_song = self.queue.popleft()
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            print(f'Hraje: {self.current_song}')
        else:
            print('Fronta je prázdná!')

    def previous_song(self, last_song):
        if last_song:
            self.queue.appendleft(self.current_song)
            self.current_song = last_song
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            print(f'Předchozí píseň: {self.current_song}')
        else:
            print('Žádná předchozí píseň!')

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.next_song()


if __name__ == "__main__":
    player = MusicPlayer()
    player.add_to_queue("song1.mp3")
    player.add_to_queue("song2.mp3")
    player.play()
    while True:
        player.handle_event()
