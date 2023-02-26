# Проектное задание четвёртого спринта

## Дополнительные требования (отметьте [Х] выбранные пункты):

- [x] (1 балл) Реализуйте возможность «удаления» сохранённого URL. Запись должна остаться, но помечаться как удалённая. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.
- [x] (2 балла) Реализуйте middleware, блокирующий доступ к сервису из запрещённых подсетей (black list).
- [x] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).


## Запуск проекта

Клонируйте проект 
```
git clone https://github.com/I-Iub/async-python-sprint-4.git
```

Перейдите в папку с проектом, создайте виртуальное окружение и активируйте его. python 3.8, ubuntu:
```
python3 -m venv venv
. venv/bin/activate
```
Установите зависимости
```
pip install --upgrade pip
pip install -r requirements.txt
```
Создайте базу данных. Например, можно создать её в docker-контейнере так:
```
docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=urls \
  -d postgres:14.5
```
В корневой директории проекта создайте файл с переменными окружения `.env` (см. пример -- `.env.example`). Укажите в нём переменную `DSN` с параметрами, соответствующими созданной базе данных.

Выполните миграции:
```
alembic upgrade head
```
Для запуска в корневой директории проекта выполните:
```
PYTHONPATH=. python3 -m src.main
```

## Запуск тестов

Создайте тестовую базу данных. Например, можно создать её в docker-контейнере:
```
docker run \
  --rm   \
  --name postgres-fastapi-tests \
  -p 65432:5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=urls \
  -d postgres:14.5
```
Если вы используете базу данных с другими параметрами, то исправьте соответствующим образом переменную `DSN` в файле `pytest.ini`, а также `DSN_TEST` в файле `.env`.

Запустите тесты:
```
PYTHONPATH=. pytest -v
```
