from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
    
class Photos(models.Model):
    image = models.ImageField(upload_to='photos/')
    caption = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    votes_count = models.PositiveIntegerField(default=0)  # Add this field

    def increment_count(self):
        # Increment the count by 1
        self.votes_count += 1
        self.save()

    def get_votes_count(self):
        return self.votes_count


class Vote(models.Model):
    voter_ip = models.GenericIPAddressField()
    photo = models.ForeignKey(Photos, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('voter_ip', 'photo')

