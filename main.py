import random
import time
import os

from utils.music_player import MusicPlayer, Song
from utils.visuals import Visuals

"===================================================="
directory = 'C:/Users/Pinki/Music/Kiss/'
songs = []
for song_name in os.listdir(directory):
    if not song_name.endswith('.mp3'):
        continue

    new_song = Song()
    filepath = os.path.join(directory, song_name)
    if os.path.exists(filepath):
        new_song.create_from_filename(filepath)
        songs.append(new_song)
    else:
        print(f"Error {filepath} not exists")

random.shuffle(songs)
"===================================================="

os.system('mode con: cols=80 lines=20')


visual = Visuals()


for song in songs:
    visual.player.add_to_queue(song)

visual.update()
visual.player.play()
visual.main_loop()



