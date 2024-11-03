from xattr import xattr
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
    def get_file_label(filepath) -> ColorLabel:
        # attrs = xattr(filepath)
        # info = attrs['com.apple.FinderInfo']
        
        key = u'com.apple.FinderInfo'
        attrs = xattr(filepath)
        color = attrs[9] >> 1 & 7
        # color = info[9] >> 1 & 7
        rawvalue = Utils.colors[color] 
        return ColorLabel(rawvalue)

    @staticmethod
    def set_label(filename, color_name):        
        key = u'com.apple.FinderInfo'
        attrs = xattr(filename)
        current = attrs.copy().get(key, chr(0)*32)
        if isinstance(current, str):
            value = chr(Utils.colors.index(color_name)*2)
            changed = current[:9] + value + current[10:]
            attrs.set(key, changed.encode())
        else:
            value = chr(Utils.colors.index(color_name)*2)
            changed = current[:9] + value.encode() + current[10:]
            attrs.set(key, changed)

