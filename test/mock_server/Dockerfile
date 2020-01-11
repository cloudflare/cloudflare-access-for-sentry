FROM python:2.7

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt
RUN ./certificate_gen.sh

ENTRYPOINT ["python"]

CMD ["cloudflare_access_mockserver.py"]