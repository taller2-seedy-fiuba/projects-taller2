FROM python:3.7.9
RUN apt-get update && apt-get install -y postgresql-client
RUN pip install poetry
WORKDIR /app
ENV POETRY_VIRTUALENVS_IN_PROJECT true
ADD . .
RUN poetry install
RUN poetry run pip install gunicorn
EXPOSE 5000
