FROM python:3.8-slim-buster

# set working directory
WORKDIR /usr/src/app

RUN apt-get update && apt install -y netcat
# RUN apk add --no-cache cifs-utils rsyn
#RUN apt-get update && apt-get install smbclient -y
# RUN apk update \
#     && apk add --virtual build-deps gcc python3-dev musl-dev \
#     && apk add postgresql-dev \
#     && pip install psycopg2 \
#     # && apk add jpeg-dev zlib-dev libjpeg \
#     # && pip install Pillow \
#     && apk del build-deps

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir /usr/src/media

COPY . .



