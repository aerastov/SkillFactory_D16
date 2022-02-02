from celery import shared_task
from django.contrib.auth.models import User, Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import Post
from django.core.mail import send_mail
from datetime import timedelta
from django.utils import timezone
import time


# @shared_task
# def add_post_send_email(category, id):
#
#     post = Post.objects.get(id=id)
#     category_group = Group.objects.get(name=category)
#     list_mail = list(User.objects.filter(groups=category_group).values_list('email', flat=True))
#     for user_email in list_mail:
#         username = list(User.objects.filter(email=user_email).values_list('username', flat=True))[0]
#         html_content = render_to_string('subscribe_new_post.html', {'post': post, 'username': username, 'category': category})
#         msg = EmailMultiAlternatives(
#             subject=f'News Portal: {category}',
#             body='',
#             from_email='newsportal272@gmail.com',
#             to=[user_email, ],
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()



# @shared_task
# def send_mail_monday_8am():
#     # Создаем список всех постов, созданных за последние 7 дней (list_week_posts)
#     now = timezone.now()
#     list_week_posts = Post.objects.filter(dateCreation__gte=now - timedelta(days=7))
#
#     for user in User.objects.filter():
#         print('\nИмя пользователя:', user)
#         print('e-mail пользователя:', user.email)
#         # Вытаскиваем список групп-категорий, на которые подписан user (list_group_item_user)
#         list_group_user = user.groups.values_list('name', flat=True)
#         print('Состоит в группах:', list(list_group_user))
#         # Вытаскиваем список ID категорий из связанной модели Category по списку групп-категорий (list_category_id)
#         list_category_id = list(Category.objects.filter(name__in=list_group_user).values_list('id', flat=True))
#         print('id категорий на которые подписан:', list_category_id)
#         # Отсеиваем посты, на которые пользователь не подписан, получаем список подписанных постов(list_week_posts_user)
#         list_week_posts_user = list_week_posts.filter(postCategory__in=list_category_id)
#         print('Список постов, созданных за интересуемый период:\n', list(list_week_posts_user))
#         if list_week_posts_user:
#             # Подготовка сообщения для отправки письма
#             list_posts = ''
#             for post in list_week_posts_user:
#                 list_posts += f'\n{post}\nhttp://127.0.0.1:8000/news/{post.id}'
#
#             send_mail(
#                 subject=f'News Portal: посты за прошедшую неделю.',
#                 message=f'Доброго дня, {user}!\nПредлагаем Вам ознакомиться с новыми постами, появившимися за последние 7 дней:\n{list_posts}',
#                 from_email='newsportal272@gmail.com',
#                 recipient_list=[user.email, ],
#             )
