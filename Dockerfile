FROM python:3.9.4
ADD . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 5000
CMD ["gunicorn", "-w", "2", "--bind", "0.0.0.0:$PORT"]