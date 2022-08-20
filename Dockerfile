FROM python:3.10-alpine

# python-ldap requirements
RUN apk update && apk add libc-dev gcc g++

# psycopg2 requirements
RUN apk add libpq python3-dev py3-pip musl-dev

RUN pip3 install --upgrade pip
COPY ./app/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /usr/app /usr/logs /usr/rules/logs /usr/inputs
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
