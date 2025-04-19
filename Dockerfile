FROM python:3.12-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update \
  && apt-get install -y gcc libpq-dev curl \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Установка poetry через pip — он встанет в /usr/local/bin
RUN pip install --upgrade pip \
  && pip install poetry

# Проверим, что он на месте
RUN which poetry && poetry --version && echo $PATH

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi --no-root

COPY . .

RUN mkdir -p /app/staticfiles && chmod -R 755 /app/staticfiles

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]


