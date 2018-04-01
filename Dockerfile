FROM ubuntu:16.04
WORKDIR /usr/src/app
ADD ./requirements.txt ./
RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential && pip install -r requirements.txt