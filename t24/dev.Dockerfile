FROM nvidia/cuda:12.3.1-base-ubuntu22.04
ENV PYTHONUNBUFFERED=1

WORKDIR /app/
COPY ./t24 .
COPY ./requirements /app/requirements
RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install python3.10-venv
RUN python3 -m venv venv
RUN venv/bin/python -m pip install --upgrade pip setuptools
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/python -m pip install -r requirements/dev.txt

CMD ["python3", "t24/manage.py", "migrate"]
CMD ["venv/bin/python", "t24/manage.py", "runserver", "localhost:8080"]
