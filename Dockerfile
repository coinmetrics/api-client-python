FROM python:3.8.12-slim

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

RUN pip install "poetry==1.1.5"
COPY pyproject.toml ./poetry.lock ./
RUN poetry config experimental.new-installer false
RUN poetry config virtualenvs.create false

RUN poetry install --no-root
RUN poetry install --no-root --extras "pandas"


COPY ./ ./

CMD [ "python" ]
