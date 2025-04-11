FROM python:3.12

# Устанавливаем Poetry
RUN pip install --upgrade pip && pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файл зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости через Poetry, без упаковки самого проекта
RUN poetry cache clear --all pypi
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi --no-root

# Копируем остальной код
COPY . .

# Создаем директорию для медиафайлов
RUN mkdir -p /code/media

# Открываем порт 8000 для взаимодействия с приложением
EXPOSE 8000
