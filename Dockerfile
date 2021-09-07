FROM python:3.8.5

RUN mkdir /yamdb_final

COPY requirements.txt /yamdb_final

RUN pip3 install -r /yamdb_final/requirements.txt

COPY . /yamdb_final
WORKDIR /yamdb_final
#CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000 
