from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserEmail(models.Model):
    email = models.EmailField(unique=True, db_index=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_email')
    display_name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'User Email'
        verbose_name_plural = 'User Emails'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.user.username}"


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100, blank=True)
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='recipes')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title