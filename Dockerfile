FROM python:3.9.4
ADD . .
RUN pip install -r requirements.txt
EXPOSE 5000
