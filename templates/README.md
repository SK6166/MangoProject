# MongoDB Library Project

## 1. Схема данных и индексы
*   **Коллекция `books`**: title (text index), author_id, year (index), genre (index).
*   **Коллекция `authors`**: name (text index), country, birth_year.

## 2. Пользователи и привилегии
*   `read_only_user` - Роль 'read'. Может только читать коллекции.
*   `read_write_user` - Роль 'readWrite'. Может создавать, изменять и удалять документы.
*   `admin_user` - Роли 'dbAdmin', 'userAdmin'. Полный доступ к управлению БД.

## 3. Запуск проекта
1. Запустить MongoDB.
2. Включить авторизацию в `mongod.cfg` (security: authorization: enabled).
3. Активировать venv `.\.venv\Scripts\activate`.
4. Выполнить `python init_mongo.py`.
5. Установить зависимости: `pip install -r requirements.txt`.
6. Запустить сервер: `python app.py`.
