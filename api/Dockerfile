FROM python:3.8-alpine

ARG run_env=dev
ENV env $run_env

WORKDIR ./usr/api
VOLUME /AllureRess
COPY requirements.txt .
RUN pip install pydantic[email]
RUN pip3 install -r requirements.txt
RUN apk update && apk upgrade && apk add bash
COPY . .

CMD python3 -m pytest -m "not $env" -s -v tests/* --alluredir=AllureRess


