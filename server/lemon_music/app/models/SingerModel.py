from django.db import models

class SingerModel(models.Model):
	"""
	歌手表
	"""

	# 歌手ID
	singer_id = models.IntegerField(primary_key=True)
	# 歌手名字 
	singer_name = models.CharField(max_length=255)

