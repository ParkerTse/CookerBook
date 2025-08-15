from django.contrib import admin
from .models import Recipe, UserEmail

admin.site.register(Recipe)
admin.site.register(UserEmail)