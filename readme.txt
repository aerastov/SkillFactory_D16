Python version 3.9.9
Django version 4.0.1

Для работы проекта необходимо:

1. Установить библиотеку bootstrap4
# pip install django-bootstrap4
2. Установить пакет allauth
# pip install django-allauth
3. Установить ckeditor
pip install django-ckeditor
4. Установить библиотеку celery
# pip install celery
6. Установить библиотеку redis
# pip install redis
7. Установить сервер redis на локальной машине
brew install redis (MacOS)
redis-server /usr/local/etc/redis.conf (Запустить сервер)
8. Установить поддержку Redis в Celery
# pip install -U "celery[redis]"
# celery -A MMORPG_board worker -l INFO -B # - команда запуска Celery




