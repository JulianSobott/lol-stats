FROM python:3.10

ENV PYTHONUNBUFFERED=0
WORKDIR /code
RUN pip install pipenv
COPY Pipfile.lock .
RUN pipenv requirements > /code/requirements.txt &&  pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

CMD ["opentelemetry-instrument", "uvicorn", "player_api.main:app", "--host", "0.0.0.0", "--port", "80", "--log-config", "player_api/logging.yml"]
