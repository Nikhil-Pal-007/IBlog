from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import BlogPost

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input-field',
        'placeholder': 'Username'
    }))

    class Meta:
        model = User
        fields = ['username']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio', 'gender']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'input-field bio-box',
                'placeholder': 'Write a bio...',
                'rows': 4
            }),
            'gender': forms.Select(attrs={
                'class': 'input-field'
            }),
        }
        

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']
        
    from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a comment...'
            })
        }