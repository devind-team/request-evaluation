FROM python:3.9.10-slim

ENV PYTHONUNBUFFERED 1
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8
ENV TZ="Europe/Moscow"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

RUN mkdir /request-evaluation

WORKDIR /request-evaluation

RUN mkdir /static && \
    apt-get update -y && \
    pip install poetry && \
    pip install --upgrade pip
#    apt-get autoremove -y && \
#    rm -rf /var/lib/apt/lists/*

COPY ./ /request-evaluation

RUN poetry install

# CMD poetry run uvicorn main:app --reload --host 0.0.0.0 --port 80