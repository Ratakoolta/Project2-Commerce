from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryType = models.CharField(max_length=20)

    def __str__(self):
        return self.categoryType

class Listing(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    available = models.CharField(max_length=20)
    description = models.CharField(max_length=2000)
    imgURL1 = models.CharField(max_length=250)
    imgURL2 = models.CharField(max_length=250)
    imgURL3 = models.CharField(max_length=250)
    isActive = models.BooleanField(default=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category= models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.name

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="autor")
    subasta = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="subasta")
    message = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.author} comment on {self.subasta}"