import pygame
import os
import random
import threading
import numpy as np
import pydub
from pydub import AudioSegment
from collections import deque


class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.queue = deque()
        self.current_song = None
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.running = True
        self.screen = pygame.display.set_mode((500, 300))
        self.clock = pygame.time.Clock()
        self.audio_data = None
        threading.Thread(target=self.get_user_input, daemon=True).start()

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
            self.load_audio_data(self.current_song)
        else:
            print('Fronta je prázdná!')

    def previous_song(self, last_song):
        if last_song:
            self.queue.appendleft(self.current_song)
            self.current_song = last_song
            pygame.mixer.music.load(self.current_song)
            pygame.mixer.music.play()
            print(f'Předchozí píseň: {self.current_song}')
            self.load_audio_data(self.current_song)
        else:
            print('Žádná předchozí píseň!')

    def shuffle_queue(self):
        random.shuffle(self.queue)
        print('Fronta byla zamíchána!')

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.next_song()

    def get_user_input(self):
        while self.running:
            command = input("Zadejte příkaz (play/pause/stop/next/shuffle/exit): ").strip().lower()
            if command == "play":
                self.play()
            elif command == "pause":
                self.pause()
            elif command == "stop":
                self.stop()
            elif command == "next":
                self.next_song()
            elif command == "shuffle":
                self.shuffle_queue()
            elif command == "exit":
                self.running = False
                pygame.mixer.quit()
                pygame.quit()
                break
            else:
                print("Neznámý příkaz!")

    def load_audio_data(self, song_path):
        try:
            audio = AudioSegment.from_file(song_path)
            samples = np.array(audio.get_array_of_samples())
            if audio.channels == 2:
                samples = samples.reshape((-1, 2))
                samples = samples.mean(axis=1)  # Převést na mono
            self.audio_data = samples
        except Exception as e:
            print(f'Chyba při načítání zvuku: {e}')
            self.audio_data = None

    def visualize(self):
        while self.running:
            self.screen.fill((0, 0, 0))
            if pygame.mixer.music.get_busy() and self.audio_data is not None:
                segment = self.audio_data[:100]
                segment = np.interp(segment, (segment.min(), segment.max()), (0, 100))
                for i, sample in enumerate(segment):
                    pygame.draw.line(self.screen, (0, 255, 0), (i * 5, 150), (i * 5, 150 - sample), 2)
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    player = MusicPlayer()
    player.add_to_queue("C:/Users/Pinki/Music/remix-edit.mp3")
    player.add_to_queue("C:/Users/Pinki/Music/remix.mp3")
    player.shuffle_queue()
    threading.Thread(target=player.visualize, daemon=True).start()
    player.play()
    while player.running:
        player.handle_event()
