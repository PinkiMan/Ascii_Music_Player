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
Filename: main.py
"""

import random
import threading

from utils.music_player import MusicPlayer
from utils.classes import SongLibrary
from utils.visual import Visuals

# TODO: finish logo printing

visual = Visuals()

visual.set_cmd_size()
visual.print_logo()

"===================================================="
library = SongLibrary()
songs = []
names = library.get_songs_names()
for name in names:
    songs.append(library.from_json_to_class_song('name', name))

random.shuffle(songs)
"===================================================="


MP = MusicPlayer()

threading.Thread(target=MP.get_user_input_2, daemon=True).start()

for song in songs:
    MP.add_to_queue(song)

MP.play()


visual.main(MP)


