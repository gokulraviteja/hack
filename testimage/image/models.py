from django.db import models

# Create your models here.
class Profile(models.Model):
    name  = models.CharField(max_length=1000)
    picture = models.ImageField(upload_to = 'images/', default = 'images/no-img.jpg')
