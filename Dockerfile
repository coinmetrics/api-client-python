FROM python:3.8.6-alpine

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev protobuf libffi-dev && \
    apk add postgresql-dev make

RUN pip install --upgrade pip

RUN pip install "poetry==1.1.11"
COPY pyproject.toml ./poetry.lock ./
RUN poetry config experimental.new-installer false
RUN poetry config virtualenvs.create false

RUN poetry install --no-root


COPY ./ ./

CMD [ "python" ]
