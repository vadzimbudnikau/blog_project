from django import forms
from .models import Post, Comment, UserProfile


class CommentForm(forms.ModelForm):
    """Form for creating a new comment."""

    class Meta:
        model = Comment
        fields = ['content']


class CommentUpdateForm(forms.ModelForm):
    """Form for updating an existing comment."""

    class Meta:
        model = Comment
        fields = ['content']


class PostForm(forms.ModelForm):
    """Form for creating a new post."""

    class Meta:
        model = Post
        exclude = ['likes', 'author']
        labels = {
            'title': 'Post Title',
            'content': 'Content'
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'cols': 60}),
        }


class PostUpdateForm(forms.ModelForm):
    """Form for updating an existing post."""

    class Meta:
        model = Post
        fields = ['title', 'content']


class UserUpdateForm(forms.ModelForm):
    """Form for updating the user profile."""

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'description', 'contact_info']
        labels = {
            'profile_picture': 'Profile Picture',
            'description': 'Description',
            'contact_info': 'Contact Information',
        }


class PostSearchForm(forms.ModelForm):
    """Form for searching posts"""

    search_query = forms.CharField(label='Search Query', max_length=100)

    class Meta:
        model = Post
        fields = ['search_query']