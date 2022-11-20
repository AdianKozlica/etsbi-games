from django.db import models

class Game(models.Model):
	name = models.CharField(max_length=255,blank=False)
	apk = models.CharField(max_length=255,blank=False)

class Watch(models.Model):
	game = models.ForeignKey(Game,on_delete=models.CASCADE)
	fingerprint = models.CharField(max_length=500,blank=False)
	date_viewed = models.DateTimeField(null=False)	