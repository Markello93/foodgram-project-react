# Foodgram
## Описание
Приложение для создания рецептов, с возможностью подписки на авторов,
добавления рецептов в избранное и корзину. Список рецептов в корзине можно
скачать в txt файл.

## Адрес сервиса
Адрес сервиса: http://158.160.14.236/

## Установка
```
git clone https://github.com/Markello93/foodgram-project-react.git
```
```
cd foodgram-project-react/infra
```

#### Создайте файл .env в директории infra/
```
nano .env
```

#### Добавьте переменные окружения:
```
SECRET_KEY = 'Ваш секретный ключ django'
DB_ENGINE = engine дб
DB_NAME = имя Вашей дб
POSTGRES_USER = имя юзера дб
POSTGRES_PASSWORD = ваш пароль для пользования 
DB_HOST = хост для базы данных
DB_PORT = порт для базы данных
```
#### Запустите сборку контейнеров docker командой:
```
docker-compose up -d
```

#### Выполните миграции:
```
docker-compose exec web python manage.py migrate
```
#### Скопируйте файлы статики в контейнер:
```
docker-compose exec web python manage.py collectstatic --no-input
```
#### Выполните импорт данных в базу данных (при необходимости):
```
docker-compose exec web python manage.py load_data
```

## Примеры
Доступ к документации API представлен по ссылке:
[http://158.160.13.46/api/docs/redoc/](http://158.160.13.46/api/docs/redoc.html)

![foodgram_workflow](https://github.com/Markello93/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)