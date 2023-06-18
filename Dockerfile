FROM python:3.11

WORKDIR /code

COPY . /code/

RUN pip install .

CMD ["prometh"]

