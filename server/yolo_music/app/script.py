import os 
import mutagen

root_path = '/Users/fengtianyu/Downloads/sample' 

invalid_files = ['.DS_Store']

def travel(path: str): 
    sub_itmes = os.listdir(path)
    for item in sub_itmes:
        # print(item) 
        full_path = path + '/' + item
        retrive_song_info(full_path)
        


def retrive_song_info(file_path):
    # songModel = SongModel()
    song = mutagen.File(file_path)
    file_type = song.mime[0]     
    print(file_type)
    print(song.info)
    print(song.keys)
    # if file_type == 'audio/ape':        
    #     song_name = song.tags['title']
    #     print('file is ape')
    #     print(song.tags)
    #     print('名字 = ' + str(song_name))
    #     print()
    # elif file_type == 'audio/flac':
    #     print('file is flac')
    #     song_name = song.tags['TITLE']
    #     artist_name = song.tags['ARTIST']
    #     print('名字 = ' + str(song_name))
    #     print('歌手 = ' + str(artist_name))
    # elif file_type == 'audio/mp3':
    #     print('file is mp3')
    #     song_name = song.tags['TIT2']
    #     artist_name = song.tags['TPE1']
    #     print('名字 = ' + str(song_name))
    #     print('歌手 = ' + str(artist_name))

    duration = song.info.length
    print('时长 = ' + str(duration))
    
    


travel(root_path)