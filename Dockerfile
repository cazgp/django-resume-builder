FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN apt-get update && apt-get -y install graphviz graphviz-dev pkg-config && rm -rf /var/lib/apt/lists/*
RUN pip install -r requirements.txt
COPY . /code/
CMD ./manage.py
