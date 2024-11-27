from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.exceptions import ValidationError

def validate_video_file(value):
    if not value.name.endswith(('.mp4', '.avi', '.mkv')):
        raise ValidationError("Invalid file format. Please upload a valid video file.")

class User(AbstractUser):
    is_creator = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Avoid conflict with auth.User
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Avoid conflict with auth.User
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

class Video(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    hashtags = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/', validators=[validate_video_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Example: 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

