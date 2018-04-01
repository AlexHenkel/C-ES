FROM python:2.7-jessie
WORKDIR /usr/src/app
ADD ./requirements.txt ./
RUN pip install -r requirements.txt