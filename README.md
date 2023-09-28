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

# Описание
[Foodgram](https://russel.fun/) - это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Функциональность проекта
- Валидация email при регистрации;
- Система восстановления пароля;
- Фильтрация по тегам;
- Пагинация;
- Обработка ошибок 404, 500;
- Админ-зона;
- Cоздание/редактирование/удаление рецепта;
- Подписка/отписка на пользователя;
- Добавление/удаление рецептов в избранное;
- Добавление/удаление рецептов в список покупок;
- Формирование списка покупок с перечнем и количеством необходимых продуктов и возможностью скачивания списка.

## Инфраструктура
- Проект работает с СУБД PostgreSQL;
- Проект запущен на сервере в Яндекс.Облаке в трёх контейнерах: Nginx, PostgreSQL и Django+Gunicorn;
- Контейнер с проектом обновляется на DockerHub;
- В Nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn;
- Данные сохраняются в volumes.

# Запуск и развертывание приложения

## В режиме разработки
- Cклонируйте данный репозиторий:
    ```bash
    git clone https://github.com/russel-07/foodgram-project.git
    ```
- Откройте проект, создайте и запустите виртуальное окружение:
    ```bash
    python -m venv venv && source venv/Scripts/activate
    ```

- Установите пакеты виртуального окружения:
    ```bash
    pip install -r requirements.txt
    ```

- Переименуйте `.env.template` в `.env`:
    ```bash
    mv ./.env.template ./.env
    ```

- Измените переменную `IS_LOCAL_ENV` в файле `settings.py` на значение `True` и сохраните изменения;

- Войдите в директорию foodgram_project и выполните миграции:
    ```bash
    cd foodgram_project && python manage.py migrate
    ```

- Выполните команду сбора статики:
    ```bash
    python manage.py collectstatic --no-input
    ```

- При необходимости заполните базу данных тестовыми данными из файла 'fixtures.json':
    ```bash
    python manage.py loaddata fixtures.json
    ```

- Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

- Запустите проект:
    ```bash
    python manage.py runserver
    ```

- В браузере по адресу [localhost:8000](http://localhost:8000/) будет доступно приложение Foodgram. Приложение будет запущено в режиме отладки с эмуляцией почтового сервера, все письма будут создаваться в директории `sent_emails`;
 
- На страницу администрирования можно войти по данным суперпользователя по адресу [localhost:8000/admin/](http://localhost:8000/admin/).

## В режиме запуска на сервере
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
