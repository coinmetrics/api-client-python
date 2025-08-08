FROM python:3.11-bookworm

ARG CM_API_KEY=""
ENV CM_API_KEY=$CM_API_KEY

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qy \
      cargo \
      make \
      postgresql-server-dev-all \
      python3-dev \
      python3-protobuf \
      build-essential \
      ;

RUN pip install --upgrade pip

RUN pip install poetry
COPY pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false

RUN poetry install --no-root --with dev

COPY ./ ./

CMD [ "python" ]
