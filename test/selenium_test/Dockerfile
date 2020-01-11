FROM python:2.7

COPY . /selenium

WORKDIR /selenium

RUN pip install -r requirements.txt

ENTRYPOINT ["./docker-entrypoint.sh"]