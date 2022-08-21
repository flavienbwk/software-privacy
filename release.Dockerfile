FROM python:3.10-alpine AS base

RUN mkdir -p /usr/app
WORKDIR /usr/app

RUN apk update && apk add python3-dev py3-pip py3-scipy gfortran build-base wget libpng-dev openblas-dev

COPY ./app /usr/app
RUN pip3 install --upgrade pip==22.2.2 && pip3 install wheel==0.37.1 && pip3 wheel . --wheel-dir=/usr/app/wheels


FROM python:3.10-alpine

ARG VERSION
RUN mkdir -p /usr/app
WORKDIR /usr/app

#RUN apk update && apk add py3-scipy

COPY --from=base /usr/app /usr/app

RUN pip3 install --upgrade pip==22.2.2 && pip3 install --no-index --find-links=/usr/app/wheels -r /usr/app/requirements.txt
RUN pip3 install -e /usr/app

RUN mkdir -p /usr/logs /usr/rules/logs /usr/inputs
ENTRYPOINT [ "python3", "-m", "software_privacy" ]
