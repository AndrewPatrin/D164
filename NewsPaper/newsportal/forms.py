from django import forms
from .models import Post, Category
from django.core.exceptions import ValidationError


class SubscribeForm(forms.Form):
    sub_category = forms.CharField(max_length=100)
    rpath = forms.CharField(max_length=100)
    """class Meta:
        model = Category
        fields = [
            'category',
        ]"""


class PostForm(forms.ModelForm):
    # request = None
    class Meta:
        model = Post
        fields = [
            'post_title',
            'post_text',
            'category',
            # 'author',
        ]
