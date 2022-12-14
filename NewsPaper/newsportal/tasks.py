from celery import shared_task
from .models import Post, Category
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime


@shared_task
def send_email_new_post(post_id, categories_ids):
    post = Post.objects.get(pk=post_id)
    for category_id in categories_ids:
        category = Category.objects.get(pk=category_id)
        category_users = category.users.all()
        for user in category_users:
            html_content = render_to_string(
                'post_message.html',
                {
                    'post': post,
                    'user': user
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"""New "{category.category}" post here - {post.post_title}""",
                body=f"Hello, {user.username}! New post in your favorite section! {post.post_text}",
                from_email='newspaper.main@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


@shared_task
def weekly_newsletter_start():
    date_now = datetime.datetime.now()
    date_weekago = date_now - datetime.timedelta(days=7)
    for category in Category.objects.all():
        weekly_newsletter_send.delay(category.pk, date_now, date_weekago)


@shared_task
def weekly_newsletter_send(category_id, date_now, date_weekago):
    category = Category.objects.get(pk=category_id)
    posts = category.post_set.filter(
        published_date__lt=date_now, published_date__gt=date_weekago)
    if posts:
        for user in category.users.all():
            html_content = render_to_string(
                'posts_message.html',
                {
                    'posts': posts,
                    'user': user,
                    'category': category.category
                }
            )
            msg = EmailMultiAlternatives(
                subject=f"""{category.category} Weekly Newsletter""",
                body=f"Hello, {user.username}! {category.category} Weekly Newsletter ",
                from_email='newspaper.main@yandex.ru',
                to=[user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            print(
                f"Done! User: {user.username} - Category: {category.category}")
        print(f"{category.category} done!")
