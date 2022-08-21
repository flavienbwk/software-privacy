FROM python:3.10-slim AS base

RUN apt-get update && apt-get install -y python3-dev python3-opencv g++ gcc make

RUN mkdir -p /usr/app/wheels
WORKDIR /usr/app

COPY ./app/requirements.txt /usr/app/requirements.txt
RUN pip3 install --upgrade pip==22.2.2 && pip3 install wheel==0.37.1 && pip3 wheel -r /usr/app/requirements.txt --wheel-dir=/usr/app/wheels


FROM python:3.10-slim

ARG VERSION
WORKDIR /usr/app

RUN apt-get update \
    && apt-get install -y python3-opencv exiftool \
    && rm -rf /var/lib/apt/lists/*

COPY --from=base /usr/app /usr/app

RUN pip3 install --upgrade pip==22.2.2 && pip3 install --no-index /usr/app/wheels/* && rm -rf /usr/app/wheels
COPY ./app /usr/app
RUN pip3 install -e /usr/app

RUN mkdir -p /usr/logs /usr/rules /usr/inputs
ENTRYPOINT [ "python3", "-m", "software_privacy" ]
