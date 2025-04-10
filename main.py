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
Filename: main.py
"""

import random
import time
import os
import threading
from mutagen.mp3 import MP3

from utils.music_player import MusicPlayer, ActualSong
from utils.visual import Visuals

# TODO: finish logo printing
# TODO: rework logo printing (add to function)
for _ in range(2):
    print()

offset = 20
with open('data/logo', 'r') as file:
    for line in file.readlines():
        print(' '*offset+line, end='')

for _ in range(1):
    print()
#time.sleep(5)


"===================================================="

#directory = 'C:/Users/Pinki/Music/Kiss/'
directory = '/Volumes/smb/Songs/Kiss/'

songs = []
for song_name in os.listdir(directory):
    if not song_name.endswith('.mp3'):
        continue

    new_song = ActualSong().empty()
    filepath = os.path.join(directory, song_name)
    if os.path.exists(filepath):
        try:
            new_song.create_from_filename(filepath)
            audio = MP3(filepath)
            new_song.duration = int(audio.info.length)
            songs.append(new_song)
            if len(songs) > 20:
                break
        except Exception as Err:
            print(Err)
    else:
        print(f"Error {filepath} not exists")

random.shuffle(songs)
"===================================================="

os.system('mode con: cols=80 lines=20')


visual = Visuals()
MP = MusicPlayer()

threading.Thread(target=MP.get_user_input, daemon=True).start()

for song in songs:
    MP.add_to_queue(song)

MP.play()

while True:
    start = time.process_time()
    MP.handle_event()

    visual.history_queue = MP.history_queue
    visual.current_song = MP.current_song
    visual.upcoming_queue = MP.upcoming_queue

    visual.update(MP.current_song)
    end = time.process_time()

    fps = 30

    if end - start < 1/fps:
        time.sleep(1/fps - (end-start))


