# Запуск приложения
## 1. Клонирование репозитория
Сначала клонируйте репозиторий:

```bash
git clone https://github.com/Similization/Task2024.git
cd myapp
```
## 2. Настройка конфигурации
Создайте файл config.yaml в корне проекта и укажите параметры для подключения к базе данных:

```yaml
database:
  user: usr
  password: pass
  dbname: task
  host: db
  port: 5432
```
## 3.1 Запуск приложения
Ввести в консоль:
```bash
python main.py
```
## 3.2 Запуск приложения с Docker
Собрать и запустить контейнеры:
```bash
docker-compose up --build
```
## 4. Остановка контейнеров
Чтобы остановить контейнеры, выполните:

```bash
docker-compose down
```
## 5. Доступ к приложению
После запуска приложение будет доступно по адресу: http://localhost:8000

## 6. Получение OpenAPI документации
Документация OpenAPI доступна по адресу:

```bash
http://localhost:8000/docs
```
Или JSON файл:

```bash
http://localhost:8000/openapi.json
```
