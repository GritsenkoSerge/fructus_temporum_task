# Тестовое задание на позицию Python backend-разработчик
[Техническое задание](./docs/technical-assignment.md)

[Запуск проекта](infra/prod/README.md)

[Запуск проекта в режиме разработчика](infra/dev/README.md)

### Деплой:
[swagger](http://bookmarks.gricen.ru/api/schema/swagger-ui/)

[redoc](http://bookmarks.gricen.ru/api/schema/redoc/)

[схема](http://bookmarks.gricen.ru/api/schema/)

### TODO
- [devops] ~~запустить проект на хостинге~~
- [devops] настроить СI/CD через GitHub Actions
- [devops] настроить доступ через HTTPS (получить сертификаты и запустить автообновление)
- [tests] написать unit-тесты на ручки
- [async] реализовать вариант когда при добавлении не нужно сразу возвращать всю информацию о закладке (в этом случае meta-информацию по ссылке можно получать асинхронно с помощью celery)
- [api] реализовать весь стандартный набор ручек для управления пользователем
- [admin] настроить панель администратора для более удобной работы (придумать требования)
