# docker build . -t flask_image
# docker run --rm --name flask_template -p 80:80 flask_image
FROM python:3.8.4

RUN mkdir /server
WORKDIR /server

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY requirements.lock .
ARG PIP_EXTRA_INDEX_URL
RUN pip install -r requirements.lock --src /usr/local/src

COPY app/ app
COPY run.py .
COPY production_files/uwsgi.ini .

# Copy production files needed
COPY production_files/nginx.conf /etc/nginx
COPY production_files/start.sh .

RUN chmod +x ./start.sh

CMD ["./start.sh"]
