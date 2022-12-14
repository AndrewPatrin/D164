from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

news = 'NW'
article = 'AR'
TYPES = [
    (news, 'News'),
    (article, 'Article')
]


class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

    def update_rating(self):
        self.author_rating = 0
        for i in self.post_set.values('post_rating'):
            self.author_rating += i['post_rating'] * 3
        for i in self.user.comment_set.values('comment_rating'):
            self.author_rating += i['comment_rating']
        for i in self.post_set.all():
            for j in i.comment_set.values('comment_rating'):
                self.author_rating += j['comment_rating']

        self.save()


class Category(models.Model):
    category = models.CharField(unique=True, max_length=100)
    users = models.ManyToManyField(User, through='Subscribers', blank=True)

    def __str__(self):
        return f'{self.category}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=news)
    published_date = models.DateTimeField(auto_now_add=True)
    post_title = models.CharField(max_length=100)
    post_text = models.TextField()
    category = models.ManyToManyField(Category, through="PostCategory")
    post_rating = models.IntegerField(default=0)

    def categories(self):
        list = self.category.values_list().values_list('category', flat=True)
        return ('{}\n'*len(list)).format(*list)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:124] + "..."

    def __str__(self):
        return f'{self.post_title}'

    def get_absolute_url(self):
        if self.type == 'NW':
            return reverse('news_detail', args=[str(self.id)])
        elif self.type == 'AR':
            return reverse('article_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        cache.delete(f'post-{self.pk}')
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        cache.delete(f'post-{self.pk}')
        super().delete(*args, **kwargs)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
