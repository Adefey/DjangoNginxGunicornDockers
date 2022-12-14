FROM python:latest
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install -y python3 git mariadb-client
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .


