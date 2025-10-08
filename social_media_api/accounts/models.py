from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", through="UserFollow"
    )


class UserFollow(models.Model):
    follower = models.ForeignKey(
        User, related_name="following_links", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="follower_links", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
