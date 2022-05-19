# Проект request-evaluation

Приложение состоит из одного сервиса разработанного на `FAST API`, который выполняет две функции:
* принимает запрос по http (url http://localhost:8095/traffic), увеличивая счетчик в базе данных;
* ежедневно в 8:00 формирует отчет (word файл) и отправляет его по электронной почте.

# Необходимые зависимости для развертки сервиса

| Зависимость                                                | Версия |
|:-----------------------------------------------------------|:------:|
| [docker](https://docs.docker.com/engine/install/ubuntu/)   | latest |
| [docker-compose](https://docs.docker.com/compose/install/) | latest |
| [PostgreSQL](https://www.postgresql.org/download/)         | latest |

# Для развертки сервиса нужно

1. Создать файл `docker-compose.yml`, пример его содержания представлен в репозитории.
2. Создать файл `.env` для необходимых переменных окружения, пример его содержания представлен в репозитории.
3. Открыть директорию, в которой находятся эти файлы, и выполнить следующею последовательность команд:
   * Для скачки сервиса
     ```shell
     sudo docker-compose pull
     ```
   * Для поднятия сервиса в контейнере
     ```shell
     sudo docker-compose up -d
     ```
   * Для выполнения миграций
   > Но перед началом миграций необходимо
   >> 3.1 Создать базу данных и дать полные права пользователю базы данных над ней
   >>  ```shell
   >>  psql -U postgres
   >>  create database database_name;
   >>  grant all privileges on database database_name to username;
   >>  grant connect on database database_name TO username;
   >>  ```
   >> 3.2 Изменить конфигурационный файл PostgreSQL, добавив в него запись:
   >> > Конфигурационный файл называется `pg_hba.conf`
   >>```shell
   >>  host    database_name         username        ip_addres_docker_container/24           md5
   >>  ```
   >> 3.3 Перезапустить PostgreSQL
   >>  ```shell
   >>  sudo service postgresql restart
   >>  ```
     ```shell
     sudo docker-compose run request-evaluation poetry run python -m alembic upgrade head
     ```
   
# Основные URL

* http://127.0.0.1:8000/traffic/
  * (POST) - принимает запрос с секретным ключем и увеличивает счетчик
* http://127.0.0.1:8000/traffic/{token_access}/
  * token_access - указывается для доступа к страницам из .env
  * (GET) - проверяет токен доступа к странице
* http://127.0.0.1:8000/identification_site/
  * форма для создания токена доступа к новому сайту
  * (POST) - отправляет название и секретный ключ 
* http://127.0.0.1:8000/identification/
  * (POST) - принимает и добавляет в бд новую запись
* http://127.0.0.1:8000/info/{identification_site}/
  * identification_site - секретный ключ сайта
  * (GET) - вывод текущей статистики 