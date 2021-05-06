FROM python:3.7.9
RUN apt-get update && apt-get install -y postgresql-client
ADD . .
RUN pip install -r requirements.txt
EXPOSE 5000
