FROM python:3.9.4
ADD . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 5000
