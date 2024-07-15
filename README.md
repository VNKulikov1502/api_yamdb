# YATUBE_API

## Описание

Проект YaMDb собирает отзывы пользователей на произведения.

## О проекте

API разработан в рамках обучения на Яндекс Практикуме по курсу python-разработчик.
Проект является учебным 

### Шаги установки

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/VNKulikov1502/api_final_yatube.git
    ```
   Перейдите в директорию проекта

2. Создайте виртуальное окружение и активируйте его:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4. Выполните миграции базы данных:
    ```bash
    python manage.py migrate
    ```

5. Создайте суперпользователя:
    ```bash
    python manage.py createsuperuser
    ```

6. Запустите сервер:
    ```bash
    python manage.py runserver
    ```
## Примеры запросов и ответов:
### GET: api/v1/titles/
```json
{
{
"count": 0,
"next": "string",
"previous": "string",
"results": [
{}
]
}
```
### POST: api/v1/titles/{title_id}/reviews/
```json
{
"id": 0,
"text": "string",
"author": "string",
"score": 1,
"pub_date": "2019-08-24T14:15:22Z"
}
```
### Полную документацию API можно получить по эндпоинту http://127.0.0.1:8000/redoc/