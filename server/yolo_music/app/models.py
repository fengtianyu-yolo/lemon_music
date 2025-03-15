from django.db import models

# Create your models here.
class SongModel(models.Model):
    song_id = models.AutoField(primary_key=True) 
    song_name = models.CharField(max_length=255)
    duration = models.IntegerField() 
    media_type = models.IntegerField() 
    sq_file_name = models.CharField(max_length=255)
    sq_file_path = models.CharField(max_length=255)
    hq_file_name = models.CharField(max_length=255)
    hq_file_path = models.CharField(max_length=255)
    cover_path = models.CharField(max_length=255, default='')
    added_time = models.DateTimeField(auto_now_add=True) 
    updated_time = models.DateTimeField(auto_now=True) 

class ArtistModel(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=255) 

class Song2ArtistModel(models.Model):
    song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
    artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)    


class DeviceModel(models.Model):    
    device_id = models.CharField(primary_key=True, max_length=255)
    device_name = models.CharField(max_length=255)

class DeviceSongsModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
    added_time = models.DateTimeField(auto_now_add=True)

# <<<<<<<<<<<<<<<<<<<<<<<< Refactor >>>>>>>>>>>>>>>>>>>>>>>>>>

class Artist(models.Model):
    name = models.CharField(max_length=255, unique=True)
    added_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)    

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    added_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

class File(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='files')
    file_path = models.CharField(max_length=1024)
    file_size = models.IntegerField()
    format_type = models.CharField(max_length=10)

class Song(models.Model):
    """歌曲基础信息"""
    title = models.CharField(max_length=255)
    cover = models.ImageField(upload_to='cover/%Y/%m/%d', blank=True, null=True)
    artists = models.ManyToManyField(Artist, related_name='songs')    
    tags = models.ManyToManyField(Tag, related_name='songs', blank=True)    
    duration = models.PositiveIntegerField(blank=True, null=True, help_text="单位：秒")
    play_count = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)    
    