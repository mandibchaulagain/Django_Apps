from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'privacy']
    privacy = forms.ChoiceField(
        choices = Post.PRIVACY_CHOICES,
        widget = forms.RadioSelect,
        initial = Post.PUBLIC,
    )
