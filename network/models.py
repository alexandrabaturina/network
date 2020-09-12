from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user} on {self.timestamp}"

class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    followed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_by')

    def __str__(self):
        return f"{self.user} is following {self.followed_by}"
