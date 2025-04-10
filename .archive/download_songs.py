#from pytube import YouTube
from pytubefix import YouTube

from youtubesearchpython import VideosSearch
import os

def Download(link,Type="Audio"):
    cwd = os.getcwd()
    cwd = os.path.dirname(cwd)
    cwd = os.path.join(cwd, 'data', 'songs', 'dowloaded')

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
    print('ose', ose)
    Output= ose
    print(f"{Input} -> {Output}")

    Link='ffmpeg -i "'+Input+'" -vn -ab 256k -ar 44100 -loglevel quiet -y "'+Output+'"'

    os.system(Link)




def Get_Link(Name):
    videosSearch = VideosSearch(Name, limit=2)
    Link=videosSearch.result()['result'][0]['link']
    return Link




FILE=open('songs.txt','r',encoding='utf-8')

for ids, Song in enumerate(FILE):
    print(ids, "downloading: ", Song)
    Download(Get_Link(Song.replace('\n', '')))


