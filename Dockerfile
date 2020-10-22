FROM python:3.8.6-alpine

ARG POETRY_VERSION=1.1.1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev protobuf libffi-dev && \
    apk add postgresql-dev make

RUN pip install --upgrade pip

RUN pip install "poetry==$POETRY_VERSION"
COPY pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false

RUN poetry install --no-root


COPY . .

CMD [ "python" ]
