FROM python:3.7-buster

COPY requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && rm -rf /tmp/*

CMD python3 /app/src/app.py