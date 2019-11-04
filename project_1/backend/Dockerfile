FROM python:3.6-alpine

RUN apk add --no-cache postgresql-libs
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip install flask psycopg2 flask-cors python-dateutil
RUN apk --purge del .build-deps

WORKDIR /app

CMD sh /app/entrypoint.sh