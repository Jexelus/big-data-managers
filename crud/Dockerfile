# Стадия 1: Установка зависимостей
FROM python:3.12-slim AS builder
WORKDIR /app
COPY req.txt .
RUN pip install --no-cache-dir -r req.txt

# Стадия 2: Финальный образ
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .
CMD ["python", "main.py"]