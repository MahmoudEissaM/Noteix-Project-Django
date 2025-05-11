from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png', blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"

class Note(models.Model):
    CATEGORY_CHOICES = [
        ('All', 'All'),
        ('Important', 'Important'),
        ('Tasks', 'Tasks'),
        ('Study', 'Study'),
        ('Personal', 'Personal'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='All')
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

class ArchivedNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    original_category = models.CharField(max_length=20)
    archived_at = models.DateTimeField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)

class ArchiveSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=50)  # Will store hashed PIN
    is_configured = models.BooleanField(default=False)
