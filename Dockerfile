FROM python:3.10-slim

RUN apt-get update && apt-get install -y python3-dev python3-opencv exiftool g++ gcc make

COPY ./app/requirements.txt /requirements.txt
RUN pip3 install --upgrade pip && pip3 install -r /requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /usr/app /usr/logs /usr/rules/logs /usr/inputs
ENTRYPOINT [ "sh", "/entrypoint.sh" ]
