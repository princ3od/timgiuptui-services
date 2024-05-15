FROM python:3.10

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get clean

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
ENV PORT 8080

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

CMD exec gunicorn --bind :"$PORT" --workers 1 --threads 8 --timeout 0 main:app