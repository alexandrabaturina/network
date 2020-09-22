from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    """ Model reprepenting a Post. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.timestamp}"

class Like(models.Model):
    """ Model representing a Like. """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_posts')

    def __str__(self):
        return f"{self.user} likes post of {self.liked_post.user} on {self.liked_post.timestamp}"

class Following(models.Model):
    """ Model representing a user following other users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")

    class Meta:
        unique_together = ("user", "following")

    def __str__(self):
        return f"{self.user} follows {self.following}"
