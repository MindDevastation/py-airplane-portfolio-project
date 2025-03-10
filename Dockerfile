FROM python:3.9-slim
LABEL authors="mindflux99@gmail.com"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/src

COPY ./src /app/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .env

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "airport.wsgi:application"]
