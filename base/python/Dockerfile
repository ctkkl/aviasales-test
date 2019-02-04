FROM python:alpine3.6

#https://gitlab.com/gitlab-org/gitlab-runner/issues/1682
ENV PYTHONDONTWRITEBYTECODE 1
#https://oncletom.io/2015/docker-encoding/
ENV LANG=C.UTF-8

RUN apk add --no-cache bash openssl openssl-dev

RUN set -ex \
      && apk add --no-cache --virtual .build-deps \
        git \
        gcc \
        libc-dev \
        linux-headers \
      \
      && pip3 install uwsgi requests bottle python-dateutil raven -I --no-cache-dir \
      && pip3 install --no-cache-dir git+https://git@github.com/kl09/envi.git \
      \
      && apk del .build-deps

COPY uwsgi.ini /uwsgi.ini
COPY start.sh /start.sh
RUN chmod a+x /start.sh
COPY start_daemon.sh /start_daemon.sh
RUN chmod a+x /start_daemon.sh

RUN echo '#!/bin/bash' >> /usr/local/bin/runtests && \
    echo 'python3 -m unittest -v $1' >> /usr/local/bin/runtests && \
    chmod a+x /usr/local/bin/runtests

EXPOSE 80

WORKDIR /var/www/
CMD ["/start.sh"]

