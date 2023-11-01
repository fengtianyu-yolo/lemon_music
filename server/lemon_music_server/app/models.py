from django.db import models

# Create your models here.
class SingerModel(models.Model):
	"""
	歌手表
	"""
	# 歌手ID
	singer_id = models.IntegerField(primary_key=True)
	# 歌手名字 
	singer_name = models.CharField(max_length=255, null=False, default='')


class SongModel(models.Model):
	"""
	歌曲模型
	"""
	# 歌曲ID
	song_id = models.IntegerField(primary_key=True)
	# 文件名
	song_name = models.CharField(max_length=255, null=False, default='')
	# 媒体类型
	media_type = models.IntegerField(null=True)
	# 歌曲时长 单位:秒
	duration = models.IntegerField(null=False, default=0)
	# 文件路径 
	file_path = models.CharField(max_length=255, null=True)
	# 文件的MD5值
	file_md5 = models.CharField(max_length=255, null=True)
	# 添加时间
	created_time = models.TimeField(auto_now_add=True)
	# 更新时间
	updated_time = models.TimeField(auto_now=True)
	# 外键，歌手。每首歌曲只有唯一的歌手 
	singer = models.ForeignKey(SingerModel, on_delete=models.CASCADE)


class UserModel(models.Model):
	"""
	用户表
	"""

	# 用户id 
	user_id = models.IntegerField(primary_key=True) 
	# 用户名 
	username = models.CharField(max_length=20)
	# 密码
	password = models.CharField(max_length=40)
	super_user = models.BooleanField()


class TagModel(models.Model):
	"""
	标签模型
	"""
	# 标签ID
	tag_id = models.IntegerField(primary_key=True)
	# 标签名字
	tag_name = models.CharField(max_length=255, null=False, default='')
	# 创建时间 
	created_time = models.DateTimeField(auto_now_add=True)
	# 更新时间
	updated_time = models.DateTimeField(auto_now=True)
	# user 一对多的关系，一个用户有多个标签，一个标签只会由一个用户创建
	user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


class SongTag(models.Model):
	"""
	歌曲和标签关联关系表
	多对多关系
	一首歌会有多个标签，一个标签会有多首歌曲
	"""
	tag = models.ForeignKey(TagModel, on_delete=models.CASCADE)
	song = models.ForeignKey(SongModel, on_delete=models.CASCADE)
