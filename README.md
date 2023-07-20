# Проект Foodgram - продуктовый помощник

<details>
    <summary><b>Проект доступен по ссылкам:</b></summary>

```
- https://foodgrambylev.ddns.net/
- https://foodgrambylev.ddns.net/admin/
```
</details>

<details>
    <summary><b>Учетная запись администратора</b></summary>

```
- логин: admin
- почта: leoohard@yandex.ru
- пароль: Bingo08bingo08
```
</details>

#### Проект Foodgram – Продуктовый помощник
На этом сервисе пользователи смогут публиковать рецепты, подписываться 
на публикации других пользователей, добавлять понравившиеся рецепты в список
«Избранное», а перед походом в магазин скачивать сводный список 
продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Что могут делать неавторизованные пользователи
- Создать аккаунт.
- Просматривать рецепты на главной.
- Просматривать отдельные страницы рецептов.
- Просматривать страницы пользователей.
- Фильтровать рецепты по тегам.
#### Что могут делать авторизованные пользователи
- Входить в систему под своим логином и паролем.
- Выходить из системы (разлогиниваться).
- Менять свой пароль.
- Создавать/редактировать/удалять собственные рецепты
- Просматривать рецепты на главной.
- Просматривать страницы пользователей.
- Просматривать отдельные страницы рецептов.
- Фильтровать рецепты по тегам.
- Работать с персональным списком избранного: добавлять в него рецепты или удалять их, просматривать свою страницу избранных рецептов.
- Работать с персональным списком покупок: добавлять/удалять любые рецепты, выгружать файл с количеством необходимых ингредиентов для рецептов из списка покупок.
- Подписываться на публикации авторов рецептов и отменять подписку, просматривать свою страницу подписок.
#### Что может делать администратор
Администратор обладает всеми правами авторизованного пользователя.
Плюс к этому он может:
- изменять пароль любого пользователя,
- создавать/блокировать/удалять аккаунты пользователей,
- редактировать/удалять любые рецепты,
- добавлять/удалять/редактировать ингредиенты.
- добавлять/удалять/редактировать теги.

Все эти функции реализованы в стандартной админ-панели Django.

### Технологии

- Python 3.9
- Django 3.2.16
- Django REST Framework 3.12.4
- Gunicorn 20.1.0
- Nginx
- PostgreSQL 13.0
- Docker

### Запуск проекта локально

- Клонирование удаленного репозитория
```bash
git clone git@github.com:LevAndreevS/foodgram-project-react.git
cd infra
```
- В директории /проекта создайте файл .env, с переменными окружения:
```bash
# secrets settings.py
SECRET_KEY=key
DEBUG=debug
ALLOWED_HOSTS=hosts
# database
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_HOST=db
DB_PORT=port
# secrets docker-compose.yml and docker-compose.production.yml ports
GATEWAY_PORT=port:port
# backend Dockerfile
GUNICORN_HOST=0.0.0.0
GUNICORN_PORT=8000
```
- Сборка и развертывание контейнеров
```bash
docker-compose up -d --build
```
- Миграции, статика выполняются автоматически. Создайте суперпользователя
```bash
docker-compose exec backend python manage.py createsuperuser
```
- Наполните базу данных ингредиентами
```bash
docker-compose exec backend python manage.py import_csv
```
- Стандартная админ-панель Django доступна по адресу [`http://localhost/admin/`](http://localhost/admin/)
- Документация к проекту доступна по адресу [`http://localhost/api/docs/`](`http://localhost/api/docs/`)

### Запуск API проекта в dev-режиме

- Клонирование удаленного репозитория (см. выше)
- Создание виртуального окружения и установка зависимостей
```bash
cd backend
python -m venv venv
. venv/Scripts/activate (windows)
. venv/bin/activate (linux)
pip install -r -requirements.txt
```
- в foodgram/setting.py замените БД на встроенную SQLite
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
- Примените миграции и соберите статику
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
```
- Наполнение базы данных ингредиентами
```bash
python manage.py import_csv
```
- Запуск сервера
```bash
python manage.py runserver 
```
