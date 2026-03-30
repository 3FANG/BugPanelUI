FROM python:3.13-alpine

WORKDIR /modsAPI

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Добавляем postgresql-client для pg_isready
RUN apk add --no-cache postgresql-client

COPY . .

CMD ["./entrypoint.sh"]