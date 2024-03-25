from django.db import models

class db(models.Model):
    ipAddress=models.CharField(max_length=25,default="Null")
    url = models.URLField(max_length = 200)
    title = models.CharField(max_length=25,default="Null")
    type = models.CharField(max_length=25,default="Null")
    quality = models.CharField(max_length=25,default="Null")
    stream= models.TextField()
