FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir locust

COPY locustfile.py .

CMD ["locust", "-f", "locustfile.py", "--host=http://crudservice:8000"]