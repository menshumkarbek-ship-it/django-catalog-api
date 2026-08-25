# Catalog API

Django + DRF сервис каталога товаров с категориями, JWT-аутентификацией и отзывами.

## Запуск локально

```powershell
Copy-Item .env.example .env
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Swagger: `http://127.0.0.1:8000/swagger/`

## Основные маршруты

- `POST /api/register/`, `POST /api/token/`, `POST /api/token/refresh/`
- `GET /api/me/`
- CRUD: `/api/categories/`, `/api/products/`, `/api/reviews/`
- `POST /api/password-reset/`, затем `POST /api/password-reset-confirm/<uid>/<token>/`

Списки используют пагинацию по 10 объектов. Для товаров доступны `search`, `category`, `price__gte`, `price__lte`. Изображения загружаются через `multipart/form-data`; разрешены JPG/PNG до 5 МБ. В development media раздается через Django.

Email по умолчанию выводится в консоль. Для SMTP заполните параметры в `.env`.

## Тесты

```powershell
pytest
```

## Docker

```powershell
Copy-Item .env.example .env
docker compose up --build
```
