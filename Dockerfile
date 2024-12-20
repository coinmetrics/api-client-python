FROM python:3.11.2-buster

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

RUN pip install "poetry==1.8.5" pytest-timeout pytest-xdist
COPY pyproject.toml ./poetry.lock ./
RUN poetry config virtualenvs.create false

RUN poetry install --no-root
RUN pip install pandas==2.2.3 numpy==1.26.4

COPY ./ ./

CMD [ "python" ]
