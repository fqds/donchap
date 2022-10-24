### в репозитории используются python 3.9 и django 4.1
# Инструкция по установке:
1) Клонируем репозиторий и создаем в папке с ним виртуальное окружение `python -m venv venv`
2) Заходим в виртуальное окружение и устанавливаем необходимые библиотеки `pip install -r requirements.txt`
3) Создаем базу данных `create database donchap_database'`, пользователя `create user django;` и выдаем права пользователю `grant all privileges on database donchap_database to django;`. Данные по умолчанию в репозитории: 
```
DB_NAME = "donchap_database"
DB_USER = "django"
DB_PASSWORD = "password"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
4) Выполняем команду `python manage.py migrate`
5) Запускаем сервер `python manage.py runserver`
