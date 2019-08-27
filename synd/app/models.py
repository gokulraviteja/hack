from django.db import models

# Create your models here.
class Profile(models.Model):
    name  = models.CharField(max_length=1000)
    email  = models.CharField(max_length=1000)
    mobile  = models.CharField(max_length=1000)
    accountno = models.CharField(max_length=1000)
    balance= models.IntegerField(default=10000)
    #picture = models.ImageField(upload_to = 'images/', default = 'images/no-img.jpg')


class Buffer(models.Model):
    mobile =models.CharField(max_length=1000)
    passcode=models.CharField(max_length=1000)
    time =models.IntegerField()
    amount=models.CharField(max_length=1000)
    expired=models.CharField(max_length=1000)


class Transactions(models.Model):
    from_User =models.CharField(max_length=1000)
    to_User =models.CharField(max_length=1000)
    time =models.CharField(max_length=1000)
    amount =models.CharField(max_length=1000)

class Groups(models.Model):
    grp_name=models.CharField(max_length=1000)
    grp_leader=models.CharField(max_length=1000)
    friends=models.CharField(max_length=1000)
