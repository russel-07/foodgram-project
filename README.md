# Foodgram

![workflow](https://github.com/russel-07/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

Сайт «Foodgram» - это продуктовый помощник.
Это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Сайт доступен по следующей ссылке: https://russel.fun/

## Запуск приложения

- Cкопируйте следующие файлы репозитория:
    - docker-compose.yaml
    - nginx.conf
    - .env.template

- Заполните файл .env.template данными:
    - SECRET_KEY необходимо сгенерировать в терминале с помощью команды:
    `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
    - В случае развертывания приложения на сервере, ALLOWED_HOSTS и CSRF_TRUSTED_ORIGINS необходимости заменить на публичный IP-адрес сервера
    - Задать для базы данных имя, пользователя и пароль: DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD
    - В данном проекте в качестве почтового сервиса используется smtp.yandex.ru. Необходимо указать свой email зарегистрированный на Яндекс.Почте в EMAIL_HOST_USER. Также необходимо сгенирривать пароль EMAIL_HOST_PASSWORD, как это сделать можно посмотреть по [ссылке] (https://proghunter.ru/articles/setting-up-the-smtp-mail-service-for-yandex-in-django?ysclid=llccswramz481083440)


- Запустите развертывание контейнеров:
    `docker-compose up -d`

- После завершения развертывания войдите в контейнер 'web' и создайте суперпользователя:
    `docker exec -it web bash`
    `cd foodgram_project`
    `python manage.py createsuperuser`

- В браузере по адресу 127.0.0.1:8000 будет доступно приложение Foodgram, по адресу 127.0.0.1:8000/admin по данным суперпользователя можно зайти на страницу администрирования;