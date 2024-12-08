from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Post, Comment, Tag
from taggit.forms import TagField

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Add email field

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'profile_picture', 'bio']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

class PostForm(forms.ModelForm):
    tags = TagField(required=False, help_text='Enter tags separated by spaces.')
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here'}),
        }

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        # Create new tags if they do not already exist
        tag_names = [tag.strip() for tag in tags]
        existing_tags = Tag.objects.filter(name__in=tag_names).values_list('name', flat=True)
        new_tags = set(tag_names) - set(existing_tags)
        for tag_name in new_tags:
            Tag.objects.create(name=tag_name)
        return tags
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(PostForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        post = super(PostForm, self).save(commit=False)
        if self.user is not None:
            post.author = self.user  # Set the user as the author
        if commit:
            post.save()  # Save the post instance
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content or content.strip() == "":
            raise forms.ValidationError("Comment content cannot be empty.")
        if len(content) < 3:
            raise forms.ValidationError("Comment content must be at least 3 characters long.")
        return content

