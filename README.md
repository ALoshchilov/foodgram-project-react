### Описание проекта:
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Доступ к проекту:
Проект временно размещен на личном VPS по адресу http://aloshchilov.hopto.org
Перенос на Яндекс.Облако будет произведен по мере приближения к инфраструктурному ревью.
Доступ к админке можно получить со следующими учетными данными:

```
Логин: admin_demo@admin.com
```

```
Пароль: QWee!@@2
```


### Запуск проекта:

Клонировать репозиторий:

```
git@github.com:ALoshchilov/foodgram-project-react.git
```

Перейти в папку с файлом docker-compose.yaml:

```
cd /c/Dev/foodgram-project-react/infra/
```

Запустить контейнеры приложения:

```
docker-compose up
```

Провести сбор статических файлов и миграции:

```
docker-compose exec backend python manage.py collectstatic
```

```
docker-compose run backend python manage.py makemigrations
```

```
docker-compose run backend python manage.py migrate
```
Не забудьте создать суперпользовавтеля и надежно сохранить его пароль

```
docker-compose exec backend python manage.py createsuperuser
```


### Описание переменных окружения

DB_ENGINE - тип используемой БД

```
DB_ENGINE=django.db.backends.postgresql
```

DB_NAME - имя БД

```
DB_NAME=postgres
```

POSTGRES_USER - имя пользователя для работы с БД

```
POSTGRES_USER=postgres
```

POSTGRES_PASSWORD - пароль пользователя для работы с БД

```
POSTGRES_PASSWORD=p0$tGre$
```

DB_HOST - имя сервера или контейнера, в котором размещена БД

```
DB_HOST=db
```

DB_PORT - порт подключения к БД

```
DB_PORT=5432
```

SECRET_KEY - последовательность для создания хэшей

```
SECRET_KEY=Hghgsfjg8^yn^##a1)ilz@4zqj=rq&agdol^##zgl9(vs
```


### Примеры вызывов API.

### Регистрация нового пользователя

Пример URL:
```
POST http://127.0.0.1/api/v1/auth/signup/
```

Тело запроса:
```
{
    "email": "string",
    "username": "string"
}
```

Ответ:
```
{
    "email": "string",
    "username": "string"
}
```


### Получение JWT-токена

Пример URL:
```
POST http://127.0.0.1/api/v1/auth/token/
```

Тело запроса:
```
{
    "username": "string",
    "confirmation_code": "string"
}
```

Ответ:
```
{
    "token": "string"
}
```


### Получение списка всех категорий

Пример URL:
```
GET http://127.0.0.1/api/v1/categories/
```

Ответ:
```
[
    {
        "count": 0,
        "next": "string",
        "previous": "string",
        "results": [
            {
                "name": "string",
                "slug": "string"
            }
        ]
    }
]
```

### Добавление новой категории

Пример URL:
```
POST http://127.0.0.1/api/v1/categories/
```

Тело запроса:
```
{
    "name": "string",
    "slug": "string"
}
```

Ответ:
```
{
    "name": "string",
    "slug": "string"
}
```


### Удаление категории

Пример URL:
```
DELETE http://127.0.0.1/api/v1/categories/{slug}/
```


### Получение списка всех жанров

Пример URL:
```
GET http://127.0.0.1/api/v1/genres/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```

### Добавление жанра

Пример URL:
```
POST http://127.0.0.1/api/v1/genres/
```

Ответ:
```
{
  "name": "string",
  "slug": "string"
}
```


### Удаление жанра

Пример URL:
```
DELETE http://127.0.0.1/api/v1/genres/{slug}/
```


### Получение списка всех произведений

Пример URL:
```
GET http://127.0.0.1/api/v1/titles/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```


### Добавление произведения

Пример URL:
```
POST http://127.0.0.1/api/v1/titles/
```

Тело запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Получение информации о произведении

Пример URL:
```
POST http://127.0.0.1/api/v1/titles/{titles_id}/
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Частичное обновление информации о произведении

Пример URL:
```
PATCH http://127.0.0.1/api/v1/titles/{titles_id}/
```

Тело запроса:
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

Ответ:
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```


### Удаление произведения

Пример URL:
```
PATCH http://127.0.0.1/api/v1/titles/{titles_id}/
```


### Получение списка всех отзывов

Пример URL:
```
GET http://127.0.0.1/api/v1/titles/{title_id}/reviews/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


### Добавление нового отзыва

Пример URL:
```
POST http://127.0.0.1/api/v1/titles/{title_id}/reviews/
```

Тело запроса:
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Получение отзыва по id

Пример URL:
```
GET http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/
```
Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Частичное обновление отзыва по id

Пример URL:
```
PATCH http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/
```

Тело запроса:
```
{
  "text": "string",
  "score": 1
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Удаление отзыва по id

Пример URL:
```
DELETE http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/
```


### Получение списка всех комментариев к отзыву

Пример URL:
```
GET http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```


### Добавление комментария к отзыву

Пример URL:
```
POST http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```

Тело запроса:
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Получение комментария к отзыву

Пример URL:
```
GET http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Частичное обновление комментария к отзыву

Пример URL:
```
PATCH http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```

Тело запроса:
```
{
  "text": "string"
}
```

Ответ:
```
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```


### Удаление комментария к отзыву

Пример URL:
```
DELETE http://127.0.0.1/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
```


### Получение списка всех пользователей

Пример URL:
```
GET http://127.0.0.1/api/v1/users/
```

Ответ:
```
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```


### Добавление пользователя

Пример URL:
```
POST http://127.0.0.1/api/v1/users/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Получение пользователя по username

Пример URL:
```
GET http://127.0.0.1/api/v1/users/{username}/
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Изменение данных пользователя по username

Пример URL:
```
PATCH http://127.0.0.1/api/v1/users/{username}/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```


### Удаление пользователя по username

Пример URL:
```
DELETE http://127.0.0.1/api/v1/users/{username}/
```


### Получение данных своей учетной записи

Пример URL:
```
GET http://127.0.0.1/api/v1/users/me/
```

Ответ:
```
{
"username": "string",
"email": "user@example.com",
"first_name": "string",
"last_name": "string",
"bio": "string",
"role": "user"
}
```


### Изменение данных своей учетной записи

Пример URL:
```
PATCH http://127.0.0.1/api/v1/users/me/
```

Тело запроса:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

Ответ:
```
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
