FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей для компиляции и Poetry
RUN apt-get update \
  && apt-get install -y gcc libpq-dev curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - \
  && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# Копируем только файл зависимостей и устанавливаем их
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

# Копируем остальной код
COPY . .

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
