FROM nvidia/cuda:12.3.1-base-ubuntu22.04
ENV PYTHONUNBUFFERED=1

RUN #apt install gcc
WORKDIR /app/
COPY ./t24 .
COPY ./requirements /app/requirements
RUN python -m venv venv
RUN venv/bin/python -m pip install --upgrade pip setuptools
RUN venv/bin/python -m pip install --upgrade pip
RUN venv/bin/python -m pip install -r requirements/dev.txt

CMD ["python3", "t24/manage.py", "migrate"]
CMD ["venv/bin/python", "t24/manage.py", "runserver", "localhost:8080"]
