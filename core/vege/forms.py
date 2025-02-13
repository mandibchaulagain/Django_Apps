from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'privacy']

    # Adding Bootstrap classes directly in the form fields
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Post Title"
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        label="Content"
    )
    privacy = forms.ChoiceField(
        choices=Post.PRIVACY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial=Post.PUBLIC,
        label="Privacy"
    )
