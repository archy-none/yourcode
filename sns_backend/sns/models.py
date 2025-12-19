import hashlib
import time

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""

    pass


class Post(models.Model):
    """Post model with SHA-256 hashed IDs"""

    id = models.CharField(max_length=64, primary_key=True, editable=False)
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    time = models.BigIntegerField()  # Unix epoch timestamp
    content = models.TextField(max_length=1000)
    liked = models.IntegerField(default=0)
    related = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )

    class Meta:
        ordering = ["-time"]  # Most recent first

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate SHA-256 hash from account ID + Unix timestamp
            if not self.time:
                self.time = int(time.time())

            hash_input = f"{self.account.id}{self.time}"
            self.id = hashlib.sha256(hash_input.encode()).hexdigest()

        super().save(*args, **kwargs)

    def to_dict(self):
        """Convert post to dictionary for JSON serialization"""
        return {
            "ID": self.id,
            "ACCOUNT": self.account.username,
            "TIME": self.time,
            "CONTENT": self.content,
            "LIKED": self.liked,
            "RELATED": self.related.id if self.related else None,
        }
