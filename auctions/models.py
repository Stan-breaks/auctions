from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing",blank=True,related_name="watchlist")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    starting_bid = models.IntegerField()
    image = models.CharField(max_length=200)
    category = models.CharField(max_length=64)
    user= models.CharField(max_length=64,default=" ")
    status=models.BooleanField(default=True)

class Bid(models.Model):
   listing = models.ForeignKey(Listing,null=True,on_delete=models.CASCADE, related_name='bids')
   user= models.CharField(max_length=64,null=True)
   bid=models.IntegerField(default=0)
   
class Comment(models.Model):
    listing = models.ForeignKey(Listing,null=True,on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=200)