FROM python:3.12-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /app/
COPY ./t24 .
COPY ./requirements /app/requirements

RUN python3 -m pip install -r requirements/dev.txt
RUN python3 t24/manage.py migrate
