FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    ufw \
    iptables \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_PORT=5000

CMD gunicorn -w 4 -b 0.0.0.0:${APP_PORT} run:app