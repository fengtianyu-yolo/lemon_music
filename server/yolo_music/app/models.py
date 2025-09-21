from django.db import models

# Create your models here.
# class SongModel(models.Model):
#     song_id = models.AutoField(primary_key=True) 
#     song_name = models.CharField(max_length=255)
#     duration = models.IntegerField() 
#     media_type = models.IntegerField() 
#     sq_file_name = models.CharField(max_length=255)
#     sq_file_path = models.CharField(max_length=255)
#     hq_file_name = models.CharField(max_length=255)
#     hq_file_path = models.CharField(max_length=255)
#     cover_path = models.CharField(max_length=255, default='')
#     added_time = models.DateTimeField(auto_now_add=True) 
#     updated_time = models.DateTimeField(auto_now=True) 

# class ArtistModel(models.Model):
#     artist_id = models.AutoField(primary_key=True)
#     artist_name = models.CharField(max_length=255) 

# class Song2ArtistModel(models.Model):
#     song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
#     artist = models.ForeignKey(ArtistModel, on_delete=models.CASCADE)    


# class DeviceModel(models.Model):    
#     device_id = models.CharField(primary_key=True, max_length=255)
#     device_name = models.CharField(max_length=255)

# class DeviceSongsModel(models.Model):
#     device = models.ForeignKey(DeviceModel, on_delete=models.CASCADE)
#     song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
#     added_time = models.DateTimeField(auto_now_add=True)

# <<<<<<<<<<<<<<<<<<<<<<<< Refactor >>>>>>>>>>>>>>>>>>>>>>>>>>

# class Artist(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     added_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)    

# class Tag(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     added_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)

# class Song(models.Model):
#     """歌曲基础信息"""
#     title = models.CharField(max_length=255)
#     cover = models.ImageField(upload_to='cover/%Y/%m/%d', blank=True, null=True)
#     artists = models.ManyToManyField(Artist, related_name='songs')    
#     tags = models.ManyToManyField(Tag, related_name='songs', blank=True)    
#     duration = models.PositiveIntegerField(blank=True, null=True, help_text="单位：秒")
#     play_count = models.IntegerField()
#     added_time = models.DateTimeField(auto_now_add=True)
#     updated_time = models.DateTimeField(auto_now=True)    
    
# class File(models.Model):
#     song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='files')
#     file_path = models.CharField(max_length=1024)
#     file_size = models.IntegerField()
#     format_type = models.CharField(max_length=10)


class Artist(models.Model):
    """歌手"""
    name = models.CharField(max_length=100, unique=True, verbose_name="歌手名")
    bio = models.TextField(blank=True, null=True, verbose_name="简介")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return self.name


class Tag(models.Model):
    """标签"""
    name = models.CharField(max_length=50, unique=True, verbose_name="标签名")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Song(models.Model):
    """歌曲基本信息"""
    title = models.CharField(max_length=200, verbose_name="歌曲名")
    artists = models.ManyToManyField(Artist, related_name="songs", verbose_name="歌手")
    cover = models.ImageField(upload_to="covers/", blank=True, null=True, verbose_name="封面图")
    duration = models.IntegerField(default=0)
    play_count = models.PositiveIntegerField(default=0, verbose_name="播放次数")
    tags = models.ManyToManyField(Tag, related_name="songs", blank=True, verbose_name="标签")
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.title


class AudioFile(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    quality = models.CharField(max_length=50)
    file = models.CharField(max_length=255, unique=True)
    size = models.BigIntegerField(default=0)

    class Meta:
        constraints = [
            # 用 song+file 作为唯一约束，显式指定名字，避免重复
            models.UniqueConstraint(fields=['song', 'file'], name='unique_song_file')
        ]

class UnmatchedMusic(models.Model):
    """
    用来记录未能成功处理的音乐文件
    """
    file_path = models.CharField(max_length=1024, help_text="音乐文件完整路径")
    file_name = models.CharField(max_length=255, help_text="音乐文件名")
    elem1 = models.CharField(max_length=255, blank=True, null=True, help_text="文件名切割后的第一个元素")
    elem2 = models.CharField(max_length=255, blank=True, null=True, help_text="文件名切割后的第二个元素")
    created_at = models.DateTimeField(auto_now_add=True, help_text="记录时间")

    def __str__(self):
        return f"{self.file_name} ({self.file_path})"