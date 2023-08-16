# Тестовое задание на позицию Python backend-разработчик
[Техническое задание](./docs/technical-assignment.md)

## Запуск проекта

### Клонировать репозиторий
```
git clone https://github.com/GritsenkoSerge/fructus_temporum_task
```
### Перейти в директорию fructus_temporum_task/infra/prod
```
cd fructus_temporum_task/infra/prod
```
### Скопировать файл `.env.example` в `.env`, при необходимости задать значения переменным
```
cp .env.example .env
```

| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- |
| DEBUG | False | Режим отладки |
| SECRET_KEY | None | `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` |
| ALLOWED_HOSTS | * | Список разрешенных хостов, указанных через пробел |
| POSTGRES_DB | bookmarks_db | Имя базы данных |
| POSTGRES_USER | bookmarks_user | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | bookmarks_pass | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | postgres | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |

### Запустить контейнер с базой данных PostgreSQL
```
docker compose up -d --build
```
### Ссылки
- Открыть страницы документации API:
  * [api.yaml](http://localhost:8080/api/schema/)
  * [swagger-ui](http://localhost:8080/api/schema/swagger-ui/)
  * [redoc](http://localhost:8080/api/schema/redoc/)
- Открыть панель администратора [localhost:8080/admin/](http://localhost:8080/admin/)
### Cоздать суперпользователя
```
docker compose exec backend bash
python manage.py createsuperuser
```


## Запуск проекта в режиме разработчика

### Клонировать репозиторий
```
git clone https://github.com/GritsenkoSerge/fructus_temporum_task
```
### Перейти в директорию проекта
```
cd fructus_temporum_task
```
### Создать/обновить виртуальное окружение с помощью poetry
```
poetry update
```
### Активировать виртуальное окружение
```
poetry shell
```
### Скопировать файл `.env.example` в `.env` и задать значения переменным
```
cp backend/.env.example backend/.env
```

| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- |
| DEBUG | False | Режим отладки |
| SECRET_KEY | None | `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` |
| ALLOWED_HOSTS | * | Список разрешенных хостов, указанных через пробел |
| POSTGRES_DB | bookmarks_db | Имя базы данных |
| POSTGRES_USER | bookmarks_user | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | bookmarks_pass | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | 127.0.0.1 | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |

### Перейти в директорию infra/dev/
```
cd infra/dev/
```
### Скопировать файл с переменными окружения
```
cp ../../backend/.env .
```
### Запустить контейнер с базой данных PostgreSQL
```
docker compose up -d
```
### Вернуться в директорию проекта
```
cd ../..
```
### Применить миграции
```
make mg
```
### Сгенерировать файл с переводами на русский язык
```
make mo
```
### Создать суперпользователя
```
make csu
```

### Запустить сервер
```
make run
```
### Ссылки
- Открыть панель администратора [localhost:8000/admin/](http://localhost:8000/admin/)
- Открыть страницы документации API:
  * [api.yaml](http://localhost:8000/api/schema/)
  * [swagger-ui](http://localhost:8000/api/schema/swagger-ui/)
  * [redoc](http://localhost:8000/api/schema/redoc/)
