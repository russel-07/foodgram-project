![example workflow](https://github.com/russel-07/foodgram-project/actions/workflows/foodgram_workflow.yml/badge.svg)

http://russel.fun

# Foodgram

Сайт «Foodgram» - это продуктовый помощник.
Это онлайн-сервис, где пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Запуск приложения

- Склонируйте данный репозиторий и откройте проект локально;
- Создайте и запустите виртуальное окружение:
    - $ python -m venv venv
    - $ source venv/Scripts/activate
- Установите пакеты виртуального окружения:
    - $ pip install -r requirements.txt
- Запустите развертывание контейнеров:
    - $ docker-compose up


При перезапуске виртуальной машины, меняется публичный IP и в этом случае необходимо обновить настройки ALLOWED_HOSTS и CSRF_TRUSTED_ORIGINS в foodgram_project/settings.py. Так же необходимо обновить значение ключа HOST в Action secrets репозитория github.com