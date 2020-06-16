FROM python:3.7.3-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev protobuf libffi-dev && \
    apk add postgresql-dev make

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python" ]
