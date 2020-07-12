FROM php:7.0-apache

RUN apt-get update
RUN apt-get install -y wget

RUN wget https://dl.influxdata.com/telegraf/releases/telegraf_1.14.5-1_amd64.deb
RUN dpkg -i telegraf_1.14.5-1_amd64.deb

ENV PROJECT_DIR=/var/www/html \
    APP_URL=localhost

RUN docker-php-ext-install mysqli gettext

COPY ./src $PROJECT_DIR
COPY /scripts/docker-entrypoint.sh /entrypoint.sh

RUN sed -i 's/\r//' /entrypoint.sh

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["run"]
