# Dockerfile

# FROM directive instructing base image to build upon
FROM python:2.7-stretch

# set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /usr/src/flask_api

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv
COPY ./Pipfile /usr/src/flask_api/Pipfile
RUN pipenv install --skip-lock --system --dev