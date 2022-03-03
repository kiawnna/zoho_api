FROM python:alpine3.7
COPY ./app /app
RUN pip install -r requirements.txt
WORKDIR /app
EXPOSE 5000
