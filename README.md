# praktikum_new_diplom
# Учебный проект
![Delete infra-dev directory](https://github.com/elina-kanz/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Описание
Учебный дипломный проект foodgram, созданный в рамках учебы на Яндекс.Практикуме. foodgram - это сервис для обмена рецептами 
блюд в котором вы можете узнать новые рецепты или запостить собственные. Так же есть дополнительные возможности: добавить 
понравившегося автора в подписки и отслеживать его творчество в новостной ленте, добавить рецепт в избранные, добавить 
рецепт в корзину, в которой затем сформировать список покупок с учетом других добавленных рецептов. 

Проект собирается через Docker на трех контейнерах:
 * backend для работы Django
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
git clone git@github.com:elina-kanz/foodgram-project-react.git
```
Образец наполнения ```foodgram-project-react/infra/.env```
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
cd foodgram-project-react/infra
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
