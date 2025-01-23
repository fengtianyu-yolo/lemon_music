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
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=255)
    device_type = models.IntegerField()    

class DeviceSongsModel(models.Model):
    device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
    song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
    play_count = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)

