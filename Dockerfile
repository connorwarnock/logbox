FROM python:2.7
MAINTAINER Connor Warnock "connorwarnock@gmail.com"
RUN apt-get update -qq
RUN apt-get install -y postgresql postgresql-contrib

WORKDIR /tmp
COPY requirements.txt ./
RUN pip install -r requirements.txt

ADD . /app
WORKDIR /app

ENTRYPOINT ["python"]
CMD ["app.py"]
