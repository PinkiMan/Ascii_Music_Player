__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "88/04/2025"
__created__ = "03/04/2025"

"""
Filename: classes.py
"""

import os
import json
import datetime


class Colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class Fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        light_grey = '\033[37m'
        darkgrey = '\033[90m'
        light_red = '\033[91m'
        light_green = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class Bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


class Queue:
    def __init__(self):
        self.queue = []

    def insert(self, item):
        self.queue.insert(0, item)

    def add(self, item):
        self.queue.append(item)

    def pop(self):
        return self.queue.pop(0)

    def last(self):
        return self.queue[0]

    def __len__(self):
        return len(self.queue)


class ActualSongObject:
    def __init__(self):
        self.name = ''  # 'Beat It'
        self.artist = ''  # 'Michael Jackson'
        self.duration = -1  # 258
        self.time = -1
        self.filename = ''
        self.start_datetime = ''
        self.skip_datetime = ''
        self.skip_at_time = -1

    def create_from_filename(self, filename):
        self.filename = filename
        self.name = '.'.join(os.path.basename(filename).split('.')[:-1])

    def empty(self):
        self.name = 'Empty song'

        return self


class Played:
    def __init__(self):
        self.list = []


class SongObject:
    def __init__(self):
        self.name = ''  # 'Beat It'
        self.artist = ''  # 'Michael Jackson'
        self.album = ''  # 'Thriller'

        self.genre = ''

        self.duration = -1  # 258

        self.filename = ''
        self.played = {}

        self.yt_link = ''
        self.yt_name = ''

        """self.played = []
        self.Published = None
        self.Playlists = []
        self.Styles = []
        self.Filename = None
        self.Title = None
        self.Author = None
        self.Age_Restriction = None
        self.URL = None"""

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)


class SongLibrary:
    def __init__(self):
        self.json_data = None
        self.filename = 'data/songs_library_first.json'
        self.song_directory = 'C:/Users/Pinki/Music/Songs/tmp/mp3/'

        if not os.path.isfile(self.filename):
            self.init_json()

        self.load_from_json()

    def load_from_json(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            self.json_data = json.load(f)

    def save_to_json(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)

    def init_json(self):
        created = datetime.datetime.today().strftime('%d/%m/%Y')

        json_string = {
            "version": "0.0.1",
            "created": created,
            "songs": []
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(json_string, f, ensure_ascii=False, indent=4)

    def add_song(self, song):
        song_json = {}

        for key in song.__dict__.keys():
            song_json[key] = getattr(song, key)

        self.json_data['songs'].append(song_json)

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.json_data, f, ensure_ascii=False, indent=4)

    def find_song_dict(self, song: ActualSongObject):
        for library_song in self.json_data['songs']:
            if library_song['name'] == song.name and library_song['artist'] == song.artist and library_song['filename'] == os.path.basename(song.filename):
                return library_song

        return None

    def write_song_played(self, song: ActualSongObject):
        song_json = self.find_song_dict(song)

        json_string = {
            "start_datetime": song.start_datetime,
            "skip_datetime": song.skip_datetime,
            "skip_at_time": song.skip_at_time
        }

        if type(song_json['played']) == dict:
            song_json['played'] = [json_string]
        else:
            song_json['played'].append(json_string)

        self.save_to_json()

    def from_json_to_class_song(self, by_value, value):
        for library_song in self.json_data['songs']:
            if library_song[by_value] == value:
                song = ActualSongObject()
                for key in library_song.keys():
                    setattr(song, key, library_song[key])

                return song

    def get_songs_names(self):
        names = []
        for library_song in self.json_data['songs']:
            names.append(library_song['name'])

        return names

if __name__ == '__main__':

    library = SongLibrary()
    #library.init_json()
    #library.load_from_json()
    #library.add_song(new_song)

    song = library.from_json_to_class_song('name', library.get_songs_names()[0])

    song.start_datetime = 'sxd'
    song.skip_datetime = 'xdaf'
    song.skip_at_time = 654

    library.write_song_played(song)

    print('xd')