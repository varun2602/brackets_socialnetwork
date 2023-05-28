from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    followers = models.IntegerField(max_length = 1000000, blank = True, null = True, default = 0)
    following = models.IntegerField(max_length = 1000000, blank = True, null = True, default = 0)
    profession = models.CharField(max_length = 20, blank = True, null = True, default = "")
    description = models.CharField(max_length = 100, blank = True, null = True, default = "")
    
    def __str__(self):
        return f"{self.id}: Username: {self.username}, Email: {self.email}"
class NewPost(models.Model):
    content = models.CharField(max_length = 300)
    timestamp = models.DateTimeField(auto_now_add = True, blank = True, null = True)
    creator = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "user_related")
    likes_number = models.IntegerField(max_length =100000, blank = True, null= True, default= 0)

    def __str__(self):
        return f"ID:{self.id}Content: {self.content}. Created at {self.timestamp}. Created by {self.creator}"

class Follow(models.Model):
    user_being_followed= models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "followed_related")
    user_following = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "following_related")
    test = models.IntegerField(max_length = 100, blank = True, null = True)

    def __str__(self):
        return f"{self.user_following.username} is following {self.user_being_followed.username}"
