import random
import time
import os
import threading
from mutagen.mp3 import MP3

from utils.music_player import MusicPlayer, ActualSong
from utils.visual import Visuals

"===================================================="
directory = 'C:/Users/Pinki/Music/Kiss/'
directory = '/Volumes/smb/Songs/'
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
    visual.update(MP.current_song, MP.history_queue, MP.upcoming_queue)
    end = time.process_time()

    fps = 30

    if end - start < 1/fps:
        time.sleep(1/fps - (end-start))


