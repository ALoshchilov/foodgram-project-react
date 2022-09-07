![status_badge](https://github.com/aloshchilov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Описание проекта:
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Доступ к проекту:
Проект временно размещен на личном VPS по адресу http://aloshchilov.hopto.org
Перенос на Яндекс.Облако, включение HTTPS, настройка dockerworkflow и секретных переменных 
репозитория будут произведены по мере приближения к инфраструктурному ревью.
Доступ к админке можно получить со следующими учетными данными:

```
URL админки: http://aloshchilov.hopto.org/admin/
```

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
### Документация

Документация доступна ссылке
```
http://aloshchilov.hopto.org/api/docs/redoc.html
```
