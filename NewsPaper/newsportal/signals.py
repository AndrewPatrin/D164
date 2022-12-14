from .models import Category, PostCategory
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .tasks import send_email_new_post

# @receiver(m2m_changed, sender = PostCategory)
# def trigger_new_post(sender, instance, action, **kwargs):
#
#     if action == 'post_add':
#         post_id = instance.id
#         categories_ids = [i for i in kwargs['pk_set']]
#         send_email_new_post.delay(post_id, categories_ids)

# post = instance
#
# for pk in kwargs['pk_set']:
#     category = Category.objects.get(pk=pk)
#     category_users = category.users.all()
#     for user in category_users:
#         html_content = render_to_string(
#             'post_message.html',
#             {
#                 'post': post,
#                 'user': user
#             }
#          )
#         msg = EmailMultiAlternatives(
#             subject=f"""New "{category.category}" post here - {post.post_title}""",
#             body=f"Hello, {user.username}! New post in your favorite section! {post.post_text}",
#             from_email='newspaper.main@yandex.ru',
#             to=[user.email]
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
