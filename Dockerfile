FROM tiangolo/uvicorn-gunicorn:python3.8
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

# Set the working directory to /app
WORKDIR /app

ADD ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY docker-compose.yaml /app
COPY docker-compose-test.yaml /app

COPY ./app /app