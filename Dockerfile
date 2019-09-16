FROM python:rc-alpine

WORKDIR /app

COPY ./*.py /app/
COPY ./requirements.txt /app/

RUN apk add --no-cache build-base libressl-dev libffi-dev musl-dev libxslt-dev && \
    pip install -r requirements.txt

CMD ["python3", "/app/main.py"]