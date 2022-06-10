# syntax=docker/dockerfile:1
FROM python:3.10

ENV PYTHONUNBUFFERED=0
WORKDIR /code
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

COPY cass_match.py /usr/local/lib/python3.10/site-packages/cassiopeia/core/match.py

ENTRYPOINT ["python", "app.py"]