from enum import Enum 

class MediaType(Enum):
    FLAC = 'flac'
    MP3 = 'mp3'
    WAV = 'wav'
    APE = 'ape'

MediaType.FLAC.code = 1
MediaType.MP3.code = 2
MediaType.WAV.code = 3
MediaType.APE.code = 4