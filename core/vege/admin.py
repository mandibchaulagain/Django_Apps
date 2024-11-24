from django.contrib import admin

# Register your models here.
from .models import Recipe, Post, Comment

admin.site.register(Recipe)
admin.site.register(Post)
admin.site.register(Comment)