from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_provider = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    id_document = models.FileField(upload_to='id_documents/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class UserReview(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    reviewee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received')
    rating = models.PositiveSmallIntegerField() # 1-5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.reviewee.username}"
