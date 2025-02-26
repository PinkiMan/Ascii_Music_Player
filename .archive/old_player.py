import os, pygame, sys


os.system('mode con: cols=80 lines=20')

Songs_Dir='C:/Users/Pinki/PycharmProjects/Hijack_Control_System/Flash/Version_2/Songs/'
# Songs_Dir='C:/Users/Pinki/PycharmProjects/TODO_MK1/TODO/Scripts/Random/Music_Player/Data/MP3/'



def Play_Song(Name,num=0):
    pygame.mixer.music.load(Songs_Dir+Name)
    Queue_Song(All_Songs[num if num<len(All_Songs) else 0])
    pygame.mixer.music.play()

def Queue_Song(Name):
    pygame.mixer.music.queue(Songs_Dir+Name)

def Get_Songs():
    List=os.listdir(Songs_Dir)
    return List


def print_songs(Songs,Offset):
    for Index in range(1, len(Songs) if len(Songs) <= 10 else 10):
        print(str(Index) + ': ' + Songs[Index - 1])




All_Songs=Get_Songs()

INIT_SONG='Highway_to_Hell.mp3'
VOLUME=0.125
NOW_PLAYING=INIT_SONG

pygame.init()
pygame.mixer.music.set_volume(VOLUME)


Play_Song(INIT_SONG)




print('-----Music player-----')
print()


print_songs(All_Songs,0)


for _ in range(4):
    print()



print('Now playing:\t\t\t\t\t\t\tVolume:')
print(' - '+INIT_SONG[0:60].ljust(63)+'- '+str(VOLUME*100)+'%')
print()





Quit = False
Paused=False
while not Quit:
    Input = input('> ')
    sys.stdout.write("\033[F")  # back to previous line
    sys.stdout.write("\033[K")


    Input=Input.split(' ')


    if Input[0] == "Quit" or Input[0]=="q" or Input[0]=="quit":     #exit
        Quit = True

    elif Input[0]=="p":     #pause / unpause
        if Paused:
            pygame.mixer.music.unpause()

        else:
            pygame.mixer.music.pause()

            Paused=True

    elif Input[0]=='v':     #volume
        if len(Input)==2:
            VOLUME=float(Input[1])/100
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
            print()
            pygame.mixer.music.set_volume(VOLUME)
        elif len(Input)==1:
            VOLUME = 0.125
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
            print()
            pygame.mixer.music.set_volume(VOLUME)

    elif Input[0]=='stop':      #stop
        pygame.mixer.music.stop()
        NOW_PLAYING=''
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")
        sys.stdout.write("\033[F")  # back to previous line
        sys.stdout.write("\033[K")
        print(' - ' + NOW_PLAYING[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
        print()

    elif Input[0]=='reset':     #reset view
        os.system('mode con: cols=80 lines=20')
        print('-----Music player-----')
        print()

        print_songs(All_Songs,0)

        for _ in range(4):
            print()

        print('Now playing:\t\t\t\t\t\t\tVolume:')
        print(' - ' + INIT_SONG[0:60].ljust(63) + '- ' + str(VOLUME * 100) + '%')
        print()

    else:
        try:
            num=int(Input[0])
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")
            NOW_PLAYING=All_Songs[num-1]
            print(' - '+NOW_PLAYING[0:60].ljust(63)+'- '+str(VOLUME*100)+'%')
            print()
            Play_Song(All_Songs[num-1],num)


        except:
            pass
