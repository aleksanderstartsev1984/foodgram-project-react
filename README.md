# praktikum_new_diplom
Foodgram это ресурс для публикации рецептов.
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на избранных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в формате pdf.

### Технологии

- Python
- JavaScript
- CSS
- HTML
- Gunicorn
- Nginx
- Node.js
- Docker

### Установка проекта локально

Склонировать репозиторий на локальную машину:
```bash
git clone git@github.com:aleksanderstartsev1984/foodgram-project-react.git
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/bin/activate
```

Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
DEBUG=True
ALLOWED_HOSTS=ВАШ IP,ВАШ ДОМЕН,localhost,127.0.0.1
TIME_ZONE=UTC
USE_TZ=True
SECRET_KEY=секретный ключ django

DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

Установить зависимости из файла requirements.txt:

```bash
cd backend/
pip install -r requirements.txt
```

Выполните миграции:

```bash
python manage.py migrate
```

Запустите сервер:
```bash
python manage.py runserver
```

### Авторы

Незнакомые мне люди из [ЯндексПрактикума](https://practicum.yandex.ru/)
и я [Александр Старцев](https://github.com/aleksanderstartsev1984)
