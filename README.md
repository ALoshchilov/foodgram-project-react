![status_badge](https://github.com/aloshchilov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
### Описание проекта:
Сайт Foodgram, «Продуктовый помощник». На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.


### Доступ к проекту:
Проект доступен по адресу http://aloshchilov.hopto.org
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


### Описание секретных переменных репозитория GitHub

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

DOCKER_USERNAME - логин в Docker Hub

```
DOCKER_USERNAME=user
```

DOCKER_PASSWORD - Пароль пользователя Docker

```
DOCKER_USERNAME=P@$$w0rd
```

HOST - Адрес или FQDN-имя продуктового сервера

```
HOST=12.24.56.78
```

SSH_KEY - Закрытый SSH-ключ для доступа к продуктовому серверу. Обязательно указание секций BEGIN и END

```
SSH_KEY=-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
......................................................................
UmoJA+AaHSWSkAAAAZQWxla3NhbmRyQERFU0tUT1AtUkxCRDVVTQEC
-----END OPENSSH PRIVATE KEY-----

```

TELEGRAM_TO - ID чата Телеграм для оповщений о завершении автоматического деплоя

```
TELEGRAM_TO=123456789
```

TELEGRAM_TOKEN - Токе доступа к боту Телеграм для оповщений о завершении автоматического деплоя

```
TELEGRAM_TOKEN=1234567890:ABCDEFGH123456789abcdefghijklmnopqrst
```

USER - Учетная запись с правом доступа к продуктовому серверу

```
USER=server_user
```