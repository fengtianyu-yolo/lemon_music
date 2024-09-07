import os 
import mutagen
from xattr import xattr

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
    
    
# travel(root_path)
    
def get_file_label():
    file_path = '/Users/fengtianyu/Downloads/IMG_7320.JPG'
    attrs = xattr(file_path)
    info = attrs['com.apple.FinderInfo']
    print(info)
    color = info[9] >> 1 & 7
    print(color)

def set_label(filename, color_name):
    colors = ['none', 'gray', 'green', 'purple', 'blue', 'yellow', 'red', 'orange']
    key = u'com.apple.FinderInfo'
    attrs = xattr(filename)
    current = attrs.copy().get(key, chr(0)*32)
    value = chr(colors.index(color_name)*2)
    changed = current[:9] + str.encode(value) + current[10:]
    attrs.set(key, changed)

get_file_label()

from enum import Enum 

class ColorLabel(Enum):
    none = 'none'
    gray = 'gray'
    green = 'green'
    purple = 'purple'
    blue = 'blue'
    yellow = 'yellow'
    red = 'red'
    orange = 'orange'

class Utils(object):
    
    colors = ['none', 'gray', 'green', 'purple', 'blue', 'yellow', 'red', 'orange']

    @staticmethod
    def get_file_label(filename) -> ColorLabel:
        attrs = xattr(filename)
        info = attrs['com.apple.FinderInfo']
        print(info)
        color = info[9] >> 1 & 7
        rawvalue = Utils.colors[color] 
        return ColorLabel(rawvalue)

    @staticmethod
    def set_label(filename, color_name):        
        key = u'com.apple.FinderInfo'
        attrs = xattr(filename)
        current = attrs.copy().get(key, chr(0)*32)
        value = chr(Utils.colors.index(color_name)*2)
        changed = current[:9] + str.encode(value) + current[10:]
        attrs.set(key, changed)



result = Utils.get_file_label('/Users/fengtianyu/Downloads/IMG_7320.JPG')

print(result)

Utils.set_label('/Users/fengtianyu/Downloads/IMG_7320.JPG', 'green')

# set_label('/Users/fengtianyu/Downloads/IMG_7320.JPG', 'green')
    
# finder_colors.set('/Users/fengtianyu/Downloads/IMG_7320.JPG', 'green')