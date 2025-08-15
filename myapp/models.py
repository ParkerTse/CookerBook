
from django.db import models

class UserEmail(models.Model):
	email = models.EmailField(unique=True)
	user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

# Create your models here.


class Recipe(models.Model):
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100, blank=True)
	ingredients = models.TextField()
	instructions = models.TextField()
	image = models.ImageField(upload_to='recipes/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.title
