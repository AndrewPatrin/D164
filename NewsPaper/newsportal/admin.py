from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['type', 'categories',
                    'post_title', 'author', 'published_date']
    list_filter = ['type', 'published_date']
    search_fields = ['post_title', 'author', 'type']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
