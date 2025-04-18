__author__ = "Pinkas Matěj"
__copyright__ = ""
__credits__ = []
__license__ = ""
__version__ = "0.1.0"
__maintainer__ = "Pinkas Matěj"
__email__ = "pinkas.matej@gmail.com"
__status__ = "Prototype"
__date__ = "18/04/2025"
__created__ = "16/04/2025"

"""
Filename: downloader.py
"""

#import shazam
import os
from pytubefix import YouTube
from youtubesearchpython import VideosSearch
from mutagen.mp3 import MP3

from utils.classes import SongObject, SongLibrary

class AMExport:
    def __init__(self):
        pass

    def get_data_from_apple_music_export(self, filename: str):
        with open(filename, 'r', encoding='utf-16') as f:
            start_line = f.readline().strip()
            categories = start_line.split('\t')





        pass

class YTDownloader:
    def __init__(self):
        self.song_tmp_directory = 'C:/Users/Pinki/Music/Songs/tmp/downloaded/'
        self.song_library_directory = 'C:/Users/Pinki/Music/Songs/tmp/mp3/'

        self.song_object = None

    def download_from_yt_link(self, link):
        pass

    def download_from_apple_music_export(self, string_of_data: str):
        data = string_of_data.split('\t')
        name_artist = f"{data[0]} by {data[1]}"

        self.song_object = SongObject()

        self.song_object.name = data[0]
        self.song_object.artist = data[1]

        link = self.get_link(name_artist)
        self.song_object.yt_link = link

        filepath = self.download_mp3(link)

        out_file = self.convert_to_mp3(filepath)

        audio = MP3(out_file)
        self.song_object.duration = int(audio.info.length)


        library = SongLibrary()
        library.add_song(self.song_object)
        print('xd')




    def get_link(self, name_artist: str):
        video_search = VideosSearch(name_artist, limit=2)
        link = video_search.result()['result'][0]['link']
        return link

    def download_mp3(self, link: str, only_audio = True):
        yt = YouTube(link)

        if only_audio:
            ys = yt.streams.filter(only_audio=True).order_by("abr")[-1]
        else:
            ys = yt.streams.get_highest_resolution()

        filepath = ys.download(output_path=self.song_tmp_directory)

        return filepath

    def convert_to_mp3(self, in_file: str):
        name = os.path.basename(in_file)
        flat_name = os.path.splitext(name)[0]
        new_filename = flat_name+'.mp3'
        out_file = os.path.join(self.song_library_directory, new_filename)

        self.song_object.filename = new_filename
        self.song_object.yt_name = flat_name

        ffmpeg_command = 'ffmpeg -i "' + in_file + '" -vn -ab 256k -ar 44100 -loglevel quiet -y "' + out_file + '"'

        os.system(ffmpeg_command)

        return out_file






if __name__ == '__main__':
    import random

    with open('../.archive/main_playlist.txt', 'r', encoding='utf-16') as file:
        start_line = file.readline().strip()
        lines = file.readlines()


    cls = YTDownloader()
    for index, line in enumerate(lines):
        name = line.split('\t')[0]
        artist = line.split('\t')[1]
        print(f"{index+1}/{len(lines)} downloading: {name} by {artist}")
        cls.download_from_apple_music_export(line.replace('\n', ''))



