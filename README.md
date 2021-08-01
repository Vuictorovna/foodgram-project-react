### Описание
Перед вами приложение «Продуктовый помощник»: сайт, на котором пользователи могут публиковать рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов.
***
Сервис «Список покупок» позволит перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

#### Найти проект можно по этому адресу http://84.252.143.117
***
Django administration:
* user: admin
* password: admin

### Технологии
* Python 3.8.5
* Django 3.2.5
* Django rest framework 3.11.0
* Gunicorn 20.1.0
* Nginx 1.19.3
* Postgres 12.4

### Команды для работы с приложением
-  Клонировать приложение к себе в репозиторий
```bash
git clone https://github.com/Vuictorovna/foodgram-project-react.git
```
- Необходимые переменные окружения, сохраненные в .env
    - DB_ENGINE
    - DB_NAME
    - POSTGRES_USER
    - POSTGRES_PASSWORD
    - DB_HOST
    - DB_PORT

- Запуск приложения
```bash
docker-compose up
```
- Сделать миграции
```bash
docker-compose exec backend python manage.py makemigrations

docker-compose exec backend python manage.py migrate --noinput
```
- Создание суперпользователя
```bash
docker-compose exec backend python manage.py createsuperuser
```
- Подготовка статики проекта
```bash
docker-compose exec backend python manage.py collectstatic --no-input
```
- Загрузка подготовленненных данных (ингредиенты)
```bash
cat /test_data/ingredients.csv | psql -c "COPY api_ingredient (name, measurement_unit) FROM STDIN WITH (FORMAT CSV, HEADER TRUE);"
```
### Авторы
Оля Сахаревич, студентка факультета Бэкэнд Яндекс.Практикум

