ENV PYTHONUNBUFFERED 1
ENV PATH /usr/local/bin:$PATH
ENV LANG C.UTF-8

RUN mkdir /requestEvaluation

WORKDIR /requestEvaluation

RUN apt-get update -y && \
    pip install poetry && \
    pip install --upgrade pip
#    apt-get autoremove -y && \
#    rm -rf /var/lib/apt/lists/*

COPY requestEvaluation/pyproject.toml /requestEvaluation

RUN poetry install

COPY /requestEvaluation /requestEvaluation

CMD poetry run uvicorn main:app --reload --host 0.0.0.0 --port 80