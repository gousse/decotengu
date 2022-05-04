FROM python:3.9-alpine
RUN apk add --no-cache R
RUN python3 -m pip install -r requirements
WORKDIR /data
