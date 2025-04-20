#from pytube import YouTube
from pytubefix import YouTube

from youtubesearchpython import VideosSearch
import os

def Download(link,Type="Audio"):
    cwd = os.getcwd()
    cwd = os.path.dirname(cwd)
    cwd = os.path.join(cwd, 'data', 'songs', 'dowloaded')
    cwd = 'C:\\Users\\Pinki\\Music\\Songs\\downloaded\\'

    yt = YouTube(link)

    # Getting the highest resolution possible
    if Type=="Audio":
        ys =yt.streams.filter(only_audio=True).order_by("abr")[-1]
    elif Type=="Video":
        ys = yt.streams.get_highest_resolution()
    #print("Downloading...")
    Filename=ys.download(output_path=cwd)

    Webm_To_MP3(Filename)

    #print("Download completed!!")


def Webm_To_MP3(filepath):
    Input=filepath
    ose = os.path.dirname(os.path.dirname(filepath))
    name = os.path.basename(filepath)
    ose = os.path.join(ose, 'mp3', os.path.splitext(name)[0]+'.mp3')

    Output= ose
    print(f"{Input} -> {Output}")

    Link='ffmpeg -i "'+Input+'" -vn -ab 256k -ar 44100 -loglevel quiet -y "'+Output+'"'

    os.system(Link)




def Get_Link(Name):
    videosSearch = VideosSearch(Name, limit=2)
    Link=videosSearch.result()['result'][0]['link']
    return Link




with open('main_playlist.txt', 'r', encoding='utf-16') as file:
    start_line = file.readline().strip()

    categories = start_line.split('\t')

    data = []
    for line in file.readlines():
        new = line.replace('\n', '').split('\t')
        line_str = f"{new[0]} by {new[1]}"
        data.append(line_str)

for song in data[:170:]:
    link = Get_Link(song)
    Download(link)
    print(f"Song: '{song}' downloaded")



"""FILE=open('main_playlist.txt','r',encoding='utf-8')

for ids, Song in enumerate(FILE):
    print(ids, "downloading: ", Song)
    Download(Get_Link(Song.replace('\n', '')))"""


