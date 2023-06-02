# praktikum_new_diplom
# Учебный проект
![Delete infra-dev directory](https://github.com/elina-kanz/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Описание
Учебный проект YaMDb, созданный в рамках Яндекс.Практикума. Создан на базе предыдущего для изучения workflow.
Проект YaMDb собирает отзывы пользователей на произведения. Произведения делятся на категории,
такие как «Книги», «Фильмы», «Музыка». Пользователи оставляют к произведениям текстовые отзывы
и ставят произведению оценку в диапазоне от одного до десяти; из пользовательских оценок
формируется усреднённая оценка произведения — рейтинг. Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


Проект собирается через Docker на трех контейнерах:
 * web для работы Django
 * db для работы postgresql
 * nginx
### Технологии
* Django 2.2.16
* django_filter 2.4.0
* djangorestframework 3.12.4
* djangorestframework_simplejwt 4.8.0
* PyJWT 2.1.0
* pytest 6.2.4
* pytest-django 4.4.0
* pytest-pythonpath 0.7.3
* python-dotenv 0.21.0
* gunicorn 20.0.4
* psycopg2-binary 2.8.6
* asgiref 3.2.10
* pytz 2020.1
* sqlparse 0.3.1
### Запуск проекта в dev-режиме
Клонируйте репозиторий
```
git clone git@github.com:elina-kanz/yamdb_final.git
```
Образец наполнения ```yamdb_final/infra/.env```
```
SECRET_KEY=ваш ключ
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=имя пользователя для
POSTGRES_PASSWORD=пароль для postgresql
DB_HOST=db
DB_PORT=порт для postgresql
```
Перейдите в папку с docker-compose.yaml и соберите контейнеры
```
cd yamdb_final/infra
docker-compose up -d --build
```
Сделайте миграции, соберите статику, при необходимости создайте суперюзера
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

Удалить контейнеры можно по команде
```
docker-compose down -v
```
