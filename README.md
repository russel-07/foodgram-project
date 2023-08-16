![workflow](https://github.com/russel-07/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)
 
# [Foodgram](https://russel.fun/)
 
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![Gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
 
[Foodgram](https://russel.fun/) - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
 
## Запуск и развертывание приложения
- Cкопируйте файлы `docker-compose.yaml`, `nginx.conf`, `.env.template` в одну директорию с помощью команды:
    ```bash
    curl -o docker-compose.yaml https://raw.githubusercontent.com/russel-07/foodgram-project/main/docker-compose.yaml \
    -o .env https://raw.githubusercontent.com/russel-07/foodgram-project/main/.env.template \
    -o nginx.conf https://raw.githubusercontent.com/russel-07/foodgram-project/main/nginx.conf
    ```
 
- Дополните `.env` значениями следующих переменных окружения:
    - Переменные `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS`, в случае развертывания приложения на удаленном сервере, необходимо заменить на публичный IP-адрес сервера;
    - В качестве переменной `EMAIL_HOST_USER` необходимо указать свой электронный адрес, зарегистрированный на [Яндекс.Почте](https://passport.yandex.ru/auth);
    - Переменная `EMAIL_HOST_PASSWORD` генерируется в настройках почтового ящика по [данной ссылке](https://id.yandex.ru/security/app-passwords). Выберите в меню «Создать пароль приложения» пункт «Почта (IMAP, POP3, SMTP)» и следуйте инструкциям.
 
- Запустите развертывание контейнеров:
    ```bash
    docker-compose up -d
    ```
 
- После завершения развертывания войдите в контейнер 'web' и создайте суперпользователя:
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```
 
- В браузере по адресу [localhost](http://localhost/) (в случае развертывания на удаленном сервере по IP-адресу сервера) будет доступно приложение Foodgram;
 
- На страницу администрирования можно войти по данным суперпользователя по адресу [localhost/admin/](http://localhost/admin/) (в случае развертывания на удаленном сервере по адресу: <IP-адрес сервера>/admin/) и при необходимости удалить тестовые данные из базы данных.