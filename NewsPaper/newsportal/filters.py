from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    published_date = DateFilter(field_name='published_date', lookup_expr=(
        'gt'), widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'post_title': ['icontains'],
            'post_text': ['icontains'],
            'category': ['exact'],
            'author': ['exact']
        }
