FROM python:3.9

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r /app/requirements.txt

COPY . /app

CMD python manage.py migrate ; python manage.py runserver 0.0.0.0:5000
