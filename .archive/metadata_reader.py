
with open('main_playlist.txt', 'r', encoding='utf-16') as file:
    start_line = file.readline().strip()

    categories = start_line.split('\t')
    data = []

    typps=[]
    idss=-5
    for line in file.readlines():
        new = line.replace('\n', '').split('\t')
        data.append(new)
        if new[idss] not in typps:
            typps.append(new[idss])

    for song in data[::-1]:
        for ids, category in enumerate(categories):
            if ids<len(song):
                #print(f"{category}-{song[ids]}")
                pass
        #input('next: ')
    print(typps)
    print('xd')





