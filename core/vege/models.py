from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,blank=True)
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe")

# Post Model
class Post(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'

    PRIVACY_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the post to the user
    privacy = models.CharField(
        max_length = 10,
        choices= PRIVACY_CHOICES,
        default= PUBLIC,
    )

    def __str__(self):
        return self.title

    # Method to get the total number of likes on a post
    def get_likes_count(self):
        return self.likes.count()

    # Method to get the total number of comments on a post
    def get_comments_count(self):
        return self.comments.count()

# Comment Model
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the comment to the user
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

# Like Model
class Like(models.Model):
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the like to the user

    class Meta:
        unique_together = ['post', 'user']  # Ensure a user can only like a post once

    def __str__(self):
        return f"Like by {self.user.username} on {self.post.title}"