### Описание/ Description
Перед вами приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
Сервис «Список покупок» позволит перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
***
Let me introduce you the "Product Assistant: Foodgram" application. This is a web-site where users can create and manage their cooking recipes collections. For instance, you can publish your own recipes attaching yummy photos of ready meals or browse other users recipes. What is more, recipes can be added to favorites and you can subscribe to publications of other authors.
Also there you might find extremely useful service - “Shopping List”,  which allow you to download a whole list of products required to prepare one or several selected dishes before going shoppping.

#### Найти проект можно по этому адресу/ Web address: http://84.252.143.117/recipes


### Технологии/ Technology:
* Python 3.8.5
* Django 3.2.5
* Django rest framework 3.11.0
* Gunicorn 20.1.0
* Nginx 1.19.3
* Postgres 12.4

### Команды для работы с приложением/ How to start:
-  Клонировать приложение к себе в репозиторий/ Clone the app to your repository
```bash
git clone https://github.com/Vuictorovna/foodgram-project-react.git
```
- Необходимые переменные окружения, сохраненные в .env/ Required environment variables saved in .env
    - DB_ENGINE
    - DB_NAME
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - DB_HOST
    - DB_PORT

- Запуск приложения/ App launch
```bash
docker-compose up
```
- Сделать миграции/ Make migrations
```bash
docker-compose exec backend python manage.py makemigrations

docker-compose exec backend python manage.py migrate --noinput
```
- Создание суперпользователя/ Create superuser
```bash
docker-compose exec backend python manage.py createsuperuser
```
- Подготовка статики проекта/ Preparing project statics
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```
- Загрузка подготовленненных данных (ингредиенты)/ Loading prepared data (ingredients)
```bash
cat /test_data/ingredients.csv | psql -c "COPY api_ingredient (name, measurement_unit) FROM STDIN WITH (FORMAT CSV, HEADER TRUE);"
```
### Авторы/ Author
Оля Сахаревич, студентка факультета Бэкэнд Яндекс.Практикум/ Volha Sakharevich, Yandex.Practicum student

