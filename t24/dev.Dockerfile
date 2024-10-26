FROM python:3.12.7-alpine
ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY ./t24 .
COPY ./requirements /app/requirements

RUN pip install --upgrade pip
RUN python3 -m pip install -r requirements/dev.txt --extra-index-url https://download.pytorch.org/whl/cpu

CMD ["python3", "t24/manage.py", "migrate"]
